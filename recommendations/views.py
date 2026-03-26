import os
import re
import numpy as np
from django.shortcuts import render
from movie.models import Movie


def cosine_similarity(a, b):
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def get_embedding(client, text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding, dtype=np.float32)


def text_based_similarity(prompt, movie):
    """Fallback similarity using keyword overlap across title, genre and description."""
    prompt_words = set(re.findall(r'\w+', prompt.lower()))
    movie_text = f"{movie.title} {movie.genre} {movie.description}".lower()
    movie_words = set(re.findall(r'\w+', movie_text))
    if not prompt_words or not movie_words:
        return 0.0
    intersection = prompt_words & movie_words
    return len(intersection) / len(prompt_words | movie_words)


def _candidate_movies(prompt):
    """Return a pre-filtered queryset of movies that share at least one keyword with the prompt."""
    from django.db.models import Q
    keywords = re.findall(r'\w+', prompt.lower())
    if not keywords:
        return Movie.objects.all()
    query = Q()
    for word in keywords:
        query |= Q(title__icontains=word) | Q(genre__icontains=word) | Q(description__icontains=word)
    qs = Movie.objects.filter(query)
    # Fall back to all movies if no pre-filtered match
    return qs if qs.exists() else Movie.objects.all()


def recommend(request):
    recommended_movie = None
    error_message = None
    prompt = ''
    used_fallback = False

    if request.method == 'POST':
        prompt = request.POST.get('prompt', '').strip()

        if prompt:
            try:
                from dotenv import load_dotenv

                load_dotenv('openAI.env')
                api_key = os.environ.get('openai_apikey')

                if not api_key:
                    # Fallback: use text-based keyword similarity
                    used_fallback = True
                    best_movie = None
                    max_similarity = -1

                    for movie in _candidate_movies(prompt):
                        similarity = text_based_similarity(prompt, movie)
                        if similarity > max_similarity:
                            max_similarity = similarity
                            best_movie = movie

                    if best_movie and max_similarity > 0:
                        recommended_movie = best_movie
                    else:
                        error_message = "No se encontraron películas en la base de datos."
                else:
                    from openai import OpenAI
                    client = OpenAI(api_key=api_key)

                    # Generate embedding for the user prompt
                    prompt_emb = get_embedding(client, prompt)

                    # Find the most similar movie
                    best_movie = None
                    max_similarity = -1

                    for movie in Movie.objects.all():
                        if movie.emb:
                            movie_emb = np.frombuffer(bytes(movie.emb), dtype=np.float32)
                            # Only compare if embedding has real data (non-zero)
                            if movie_emb.shape[0] > 0 and np.any(movie_emb):
                                similarity = cosine_similarity(prompt_emb, movie_emb)
                                if similarity > max_similarity:
                                    max_similarity = similarity
                                    best_movie = movie

                    if best_movie:
                        recommended_movie = best_movie
                    else:
                        error_message = (
                            "No se encontraron películas con embeddings. "
                            "Ejecuta: python manage.py movie_embeddings"
                        )

            except ImportError:
                error_message = "Librería OpenAI no instalada. Ejecuta: pip install openai"
            except Exception as e:
                error_message = f"Error al generar recomendación: {str(e)}"
        else:
            error_message = "Por favor ingresa un tema o descripción para buscar."

    return render(request, 'recommendations/recommend.html', {
        'recommended_movie': recommended_movie,
        'prompt': prompt,
        'error_message': error_message,
        'used_fallback': used_fallback,
    })
