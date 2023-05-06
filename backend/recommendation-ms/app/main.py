import httpx
from neo4j import GraphDatabase
import requests
from fastapi import FastAPI, Header, Response, Request
from app import services
from app import neo4j_db


app = FastAPI()

driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "mypassword"))


TMDB_API_ENDPOINT = "https://api.themoviedb.org/3"
TMDB_API_KEY = "9be9f81b03a97c8ad1b8a4a41fb190bd"

@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: int, num_recomendations: int = 10):
    try:
        try:
            records1 = neo4j_db.recs_based_onother_users(driver.session(), user_id)
        except neo4j.exceptions.ClientError:
            # I have no idea where this error comes from ... 
            return {f'Not valid UID ' : user_id}

        to_collect_from_tmdb = num_recomendations-len(records1)

        for_imdb = neo4j_db.recs_based_onuser_watchs(driver.session(), user_id)
        
        
        fromimdb_ids = services.tmdb_recs_us1(for_imdb, user_id, for_imdb, records1, TMDB_API_KEY, TMDB_API_ENDPOINT, num_recomendations)
        
        services.tmdb_recs_popular(TMDB_API_KEY, TMDB_API_ENDPOINT, for_imdb, records1, fromimdb_ids, num_recomendations)

        return {'recommendations films ' : f'{records1 + fromimdb_ids}'}

    except requests.exceptions.JSONDecodeError:
        return {f'No such user in db': None}


@app.post("/interactions")
async def add_interaction(request: Request):
    data = await request.json()
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    action = data.get('action')
    rating = ''
    if action == 'rated':
        rating = data.get('rating')
    genres = services.return_movie_genres(movie_id, TMDB_API_KEY)

    if action == 'liked':
        neo4j_db.add_liked_action(user_id, movie_id, driver.session(), genres)

    elif action == 'rated':
        neo4j_db.add_rated_action(user_id, movie_id, driver.session(), rating, genres)

    elif action == 'watched':
        neo4j_dbv.add_watched_action(user_id, movie_id, driver.session(), genres)

    else:
        return {"message": f"Invalid action: {action}"}


    return {"message": "Interaction added successfully"}
