

import httpx
import neo4j
import requests
from fastapi import FastAPI, Header, Response, Request

from repository.repo import RepositorySingleton


app = FastAPI()


async def other_users_likes(user_id, driver):
    try:
        reps = RepositorySingleton(user_id=user_id, driver=driver)
        records1 = reps.recs_based_onother_users()
        return (True, records1)
    except neo4j.exceptions.ClientError:
        return (False, [])

async def collect_from_tmdb(user_id, driver, records1, num_recomendations):
    to_collect_from_tmdb = num_recomendations-len(records1)
    reps = RepositorySingleton(user_id=user_id, driver=driver)
    for_imdb = reps.recs_based_onuser_watchs()
    fromimdb_ids = reps.tmdb_recs_us1(for_imdb=for_imdb, records1=records1, num_recomendations=to_collect_from_tmdb)
    lst = reps.tmdb_recs_popular()
        
    result_list = records1[:num_recomendations//2] + fromimdb_ids + lst
    return result_list


async def get_whole_recs(user_id, driver, num_recomendations):
    records1_tuple = await other_users_likes(user_id, driver)
    if records1_tuple[0]:
        records1 = records1_tuple[1]
        result_recs = await collect_from_tmdb(user_id, driver, records1, num_recomendations)
        return (True, result_recs)
    else:
        return (False, [])


async def interaction_add(action, user_id, movie_id, driver, rating=None):

    n4j_actions = RepositorySingleton(user_id=user_id, driver=driver)
    genres = n4j_actions.return_movie_genres(movie_id)

    if action == 'liked':
        n4j_actions.add_liked_action(genres, user_id)
        return True

    elif action == 'rated':
        n4j_actions.add_rated_action(movie_id, rating, genres)
        return True

    elif action == 'watched':
        n4j_actions.add_watched_action(movie_id, genres)
        return True

    else:
        return False
