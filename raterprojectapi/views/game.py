"""View module for handling requests about games"""
from raterprojectapi.models.game_categories import GameCategory
from raterprojectapi.models.categories import Category
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

    def retrieve(self, request, pk):

        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk):

        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        games = Game.objects.all()

        gamecategory = self.request.query_params.get('category', None)
        if gamecategory is not None:
            games = games.filter(categories__id=gamecategory)

        serializer = GameSerializer(
            games, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def update(self, request, pk):

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.release = request.data["release"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.duration = request.data["duration"]
        game.age = request.data["age"]
        gameplayer = Player.objects.get(pk=request.data["playerId"])
        game.player = gameplayer
        gamecategory = Category.objects.get(pk=request.data['categoryId'])
        game.categories.add(gamecategory)
        game.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')


class GameSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'release', 'number_of_players', 'duration', 'age', 'player', 'categories')
        # depth = 1

