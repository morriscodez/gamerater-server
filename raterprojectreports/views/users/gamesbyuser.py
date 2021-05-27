import sqlite3
from django.shortcuts import render
from raterprojectapi.models import Game
from raterprojectreports.views import Connection

def usergame_list(request):
    if request.method == 'GET':

        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                g.id,
                g.title,
                g.description,
                g.designer,
                g.release,
                g.number_of_players,
                g.duration,
                g.age,
                g.player_id,
                u.id user_id,
                u.first_name || ' ' || u.last_name AS full_name
            FROM
                raterprojectapi_game g
            JOIN
                raterprojectapi_player p on g.player_id = p.id
            JOIN
                auth_user u ON p.user_id = u.id
            """)

            dataset = db_cursor.fetchall()

            games_by_user = {}

            for row in dataset:

                game = Game()
                game.title = row["title"]
                game.description = row["description"]
                game.designer = row["designer"]
                game.release = row["release"]
                game.number_of_players = row["number_of_players"]
                game.duration = row["duration"]
                game.age = row["age"]

                uid = row["user_id"]

                if uid in games_by_user:

                    games_by_user[uid]['games'].append(game)

                else:
                    games_by_user[uid] = {}
                    games_by_user[uid]["id"] = uid
                    games_by_user[uid]["full_name"] = row["full_name"]
                    games_by_user[uid]["games"] = [game]

        list_of_users_with_games = games_by_user.values()

        template = 'users/list_with_games.html'
        context = {
            'usergame_list': list_of_users_with_games
        }

        return render(request, template, context)