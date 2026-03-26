
from django.db import models
import numpy as np


def get_default_embedding():
    return np.zeros(1536, dtype=np.float32).tobytes()


class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie/images/', blank=True, null=True, default=None)
    emb = models.BinaryField(default=get_default_embedding, blank=True)

    def __str__(self):
        return self.title
