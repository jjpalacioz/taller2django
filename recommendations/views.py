import os
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


def recommend(request):
    recommended_movie = None
    error_message = None
    prompt = ''

    if request.method == 'POST':
        prompt = request.POST.get('prompt', '').strip()

        if prompt:
            try:
                from openai import OpenAI
                from dotenv import load_dotenv

                load_dotenv('openAI.env')
                api_key = os.environ.get('openai_apikey')

                if not api_key:
                    error_message = "API key not configured. Please set openai_apikey in openAI.env file."
                else:
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
                            "No movies with embeddings found. "
                            "Run: python manage.py movie_embeddings"
                        )

            except ImportError:
                error_message = "OpenAI library not installed. Run: pip install openai"
            except Exception as e:
                error_message = f"Error generating recommendation: {str(e)}"
        else:
            error_message = "Please enter a search prompt."

    return render(request, 'recommendations/recommend.html', {
        'recommended_movie': recommended_movie,
        'prompt': prompt,
        'error_message': error_message,
    })
