
from django.core.management.base import BaseCommand
from movie.models import Movie
import json, os
class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        path=os.path.join(os.getcwd(),'movies.json')
        with open(path) as f:
            data=json.load(f)
        for m in data[:100]:
            Movie.objects.get_or_create(
                title=m['title'],
                genre=m['genre'],
                year=int(m['year']),
                description=m['description']
            )
        self.stdout.write(self.style.SUCCESS('Movies loaded'))
