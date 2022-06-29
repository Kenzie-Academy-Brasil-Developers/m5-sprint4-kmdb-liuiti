from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=127)

    movies = models.ManyToManyField("movies.Movie", related_name="genres")

    def __repr__(self):
        return f"{self.id} - {self.name}"