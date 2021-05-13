"""View module for handling requests about games"""
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterprojectapi.models import Game, Player

class GameView(ViewSet):

    def create(self, request):

        game = Game()
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.release = request.data["release"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.duration = request.data["duration"]
        game.age = request.data["age"]
        gameplayer = Player.objects.get(pk=request.data["playerId"])
        game.player = gameplayer

        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason: ex.message"}, status=status.HTTP_400_BAD_REQUEST)