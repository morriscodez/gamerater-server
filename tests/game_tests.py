import json
from rest_framework import status
from rest_framework.test import APITestCase
from raterprojectapi.models import Game, Category


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """

        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8",
            "email": "steve@stevebrownloee.com",
            "address": "steve@stevebrownlee.com",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee"
        }

        #initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)
        
        #Store the auth token
        self.token = json_response["token"]

        #Assert that a user was created
        #TODO: add 201 code to register user viewset
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        categories = Category()
        categories.label = "Board game"
        categories.save()

    
    def test_create_game(self):
        """ 
        Ensure we can create a new game
        """

        url = "/games"
        data = {
            "title": "Ticket To Ride",
            "description": "fun",
            "designer": "Hasbro",
            "release": "2010-01-01",
            "numberOfPlayers": 6,
            "duration": "90",
            "age": "10",
            "playerId": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        response = self.client.post(url, data, format="json")

        json_response = json.loads(response.content)

        self.assertEqual(json_response["title"], "Ticket To Ride")
        self.assertEqual(json_response["description"], "fun")
        self.assertEqual(json_response["designer"], "Hasbro")
        self.assertEqual(json_response["release"], "2010-01-01")
        self.assertEqual(json_response["number_of_players"], 6)
        self.assertEqual(json_response["duration"], "90")
        self.assertEqual(json_response["age"], "10")
        self.assertEqual(json_response["player"], 1)
    
    
    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the db with a game

        game = Game()
        game.title = "Ticket To Ride"
        game.description = "Become a train tycoon and run your friends out of business"
        game.designer = "Hasbro"
        game.release = "2010-01-01"
        game.number_of_players = 6
        game.duration = "90"
        game.age = "10"
        game.player_id = 1

        game.save()

        #to set it we need the game ID first so keep it after the save()
        game.categories.set([1])

        game.save()
        
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        response = self.client.get(f"/games/{game.id}")

        json_response = json.loads(response.content)

        self.assertEqual(json_response["title"], "Ticket To Ride")
        self.assertEqual(json_response["description"], "Become a train tycoon and run your friends out of business")
        self.assertEqual(json_response["designer"], "Hasbro")
        self.assertEqual(json_response["release"], "2010-01-01")
        self.assertEqual(json_response["number_of_players"], 6)
        self.assertEqual(json_response["duration"], "90")
        self.assertEqual(json_response["age"], "10")
        self.assertEqual(json_response["categories"][0]["id"], 1)

    
    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """

        game = Game()
        game.player_id = 1
        game.title = "Resistance"
        game.designer = "Hasbro"
        game.description = "Who can lie the best"
        game.release = "2009-01-01"
        game.number_of_players = 7
        game.duration = "30"
        game.age = 12
        game.save()
        
    
        game.categories.set([1])
        
        

        data = {
            "title": "Resistance!",
            "designer": "Lego",
            "description": "Lying to your friends",
            "numberOfPlayers": 8,
            "release": "2009-01-01",
            "duration": "90",
            "age": "16",
            "playerId": 1,
            "categoryId": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["title"], data["title"])
        self.assertEqual(json_response["designer"], data["designer"])
        self.assertEqual(json_response["description"], data["description"])
        self.assertEqual(json_response["number_of_players"], data["numberOfPlayers"])
        self.assertEqual(json_response["release"], data["release"])
        self.assertEqual(json_response["duration"], data["duration"])
        self.assertEqual(json_response["age"], data["age"])
        self.assertEqual(json_response["player"], data["playerId"])
        self.assertEqual(json_response["categories"][0]["id"], data["categoryId"])

    
    def test_delete_game(self):
        """
        Ensure we can delete an existing game
        """

        game = Game()
        game.player_id = 1
        game.title = "Resistance"
        game.designer = "Hasbro"
        game.description = "Who can lie the best"
        game.release = "2009-01-01"
        game.number_of_players = 7
        game.duration = "30"
        game.age = 12
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)