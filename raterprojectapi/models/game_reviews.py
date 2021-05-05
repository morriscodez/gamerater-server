from django.db import models
from django.db.models.fields import CharField

class GameReview(models.Model):

    review = CharField(max_length=50)
    rating = models.IntegerField()
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)