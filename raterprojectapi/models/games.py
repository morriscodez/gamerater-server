from django.db import models
from django.db.models.fields import CharField

class Game(models.Model):

    title = CharField(max_length=50)
    description = models.TextField()
    designer = CharField(max_length=50)
    release = models.DateField()
    number_of_players = models.IntegerField()
    duration = CharField(max_length=50)
    age = CharField(max_length=50)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    categories = models.ManyToManyField("Category", through="GameCategory", related_name="games")