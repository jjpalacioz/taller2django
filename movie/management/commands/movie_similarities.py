import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv


class Command(BaseCommand):
    help = "Compare two movies and a prompt using OpenAI embeddings and cosine similarity"

    def handle(self, *args, **kwargs):
        # Load OpenAI API key
        load_dotenv('openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        # Select two movies to compare
        try:
            movie1 = Movie.objects.get(title="La lista de Schindler")
            movie2 = Movie.objects.get(title="El club de la pelea")
        except Movie.DoesNotExist as e:
            self.stderr.write(f"Movie not found: {e}")
            self.stderr.write(
                "Make sure to load the movies with 'python manage.py add_movies_db' "
                "and run 'python manage.py update_movies_from_csv' to apply the correct titles."
            )
            return

        def get_embedding(text):
            response = client.embeddings.create(
                input=[text],
                model="text-embedding-3-small"
            )
            return np.array(response.data[0].embedding, dtype=np.float32)

        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        # Generate embeddings for both movies
        self.stdout.write(f"Generating embedding for: {movie1.title}")
        emb1 = get_embedding(movie1.description)

        self.stdout.write(f"Generating embedding for: {movie2.title}")
        emb2 = get_embedding(movie2.description)

        # Compute similarity between the two movies
        similarity = cosine_similarity(emb1, emb2)
        self.stdout.write(f"\n🎬 Similaridad entre '{movie1.title}' y '{movie2.title}': {similarity:.4f}")

        # Compare against a prompt
        prompt = "película sobre la Segunda Guerra Mundial"
        self.stdout.write(f"\nGenerando embedding para el prompt: '{prompt}'")
        prompt_emb = get_embedding(prompt)

        sim_prompt_movie1 = cosine_similarity(prompt_emb, emb1)
        sim_prompt_movie2 = cosine_similarity(prompt_emb, emb2)

        self.stdout.write(f"📝 Similitud prompt vs '{movie1.title}': {sim_prompt_movie1:.4f}")
        self.stdout.write(f"📝 Similitud prompt vs '{movie2.title}': {sim_prompt_movie2:.4f}")
