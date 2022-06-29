from django.db import models

class RecomendationReview(models.TextChoices):
    MUST_WATCH = ("Must Watch",)
    SHOULD_WATCH = ("Should Watch",)
    AVOID_WATCH = ("Avoid Watch",)
    DEFAULT = ("No Opinion",)

class Review(models.Model):
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField(default=False)
    recomendation = models.CharField(
        max_length=50,
        choices=RecomendationReview.choices,
        default=RecomendationReview.DEFAULT
    )

    movie = models.ForeignKey("movies.Movie", related_name="reviews", on_delete=models.CASCADE)
    critic = models.ForeignKey("users.User", related_name="reviews", on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.id} - {self.review}"