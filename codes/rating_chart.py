from collections import namedtuple
import datetime
import math
import os
import sys
import asciichartpy as ac
import requests

USERNAME = 'dyst0rti0n'
TIME_CLASS = 'blitz'
RULES = 'chess' 
NGAMES = 100
headers = {"User-Agent": "LichessRatingRefresh/1.0 dystorti0n@proton.me"}
GAMES_URL = 'https://lichess.org/api/games/user/{user}'

def get_filtered_games() -> list:
    params = {
        'max': NGAMES,
        'perfType': TIME_CLASS,
        'pgnInJson': 'true',
        'clocks': 'false',
        'evals': 'false',
        'opening': 'false'
    }
    response = requests.get(url=GAMES_URL.format(user=USERNAME), headers=headers, params=params, stream=True)
    games = []
    for line in response.iter_lines():
        if line:
            games.append(requests.utils.json.loads(line))
    _filtered_games = list(filter(lambda game: game['variant'] == RULES, games))
    return _filtered_games[::-1]

def get_ratings_from_games(games: list) -> list:
    ratings = []
    for game in games:
        if game['players']['white']['user']['name'].lower() == USERNAME.lower():
            ratings.append(game['players']['white']['rating'])
        else:
            ratings.append(game['players']['black']['rating'])
    return ratings[::-1]

def main():
    games = get_filtered_games()
    if games is not None:
        games = games[:NGAMES]
    ratings_list = get_ratings_from_games(games)
    return ac.plot(ratings_list, {'height': 15})

if __name__ == "__main__":
    plot = main()
    print(plot)
