from django.db import models

class GamePictures(models.Model): 

    img = models.URLField()
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)