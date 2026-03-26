import os
from django.core.management.base import BaseCommand
from movie.models import Movie


class Command(BaseCommand):
    help = "Update all movie images in the database from the media/movie/images/ folder"

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'

        if not os.path.exists(images_folder):
            self.stderr.write(f"Images folder '{images_folder}' not found.")
            return

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in the database")

        updated_count = 0

        for movie in movies:
            # Expected filename format: m_MOVIE_TITLE.png
            image_filename = f"m_{movie.title}.png"
            image_full_path = os.path.join(images_folder, image_filename)

            if os.path.exists(image_full_path):
                # Relative path for the ImageField
                image_relative_path = os.path.join('movie/images', image_filename)
                movie.image = image_relative_path
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
            else:
                self.stderr.write(f"Image not found for: {movie.title} (expected: {image_full_path})")

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies with images."))
