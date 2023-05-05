
import httpx
from neo4j import GraphDatabase
import requests
from fastapi import FastAPI, Header, Response, Request

def tmdb_recs_us1(user_movies, uid, for_imdb, records1,  tmdb_key, tmdb_endpoint):
    fromimdb_ids = []
    to_collect_from_tmdb = 10 - len(records1)
    if len(for_imdb)>0:
        from_imdb_recomendations = []
        for tmdb_id in for_imdb:
            response = requests.get(f"{tmdb_endpoint}/movie/{tmdb_id}/recommendations",
                                    params={"api_key": tmdb_key})
            if response.status_code == 200:
                results = response.json().get("results", [])
                for result in results:
                    if result["id"] not in records1 and result not in from_imdb_recomendations and result not in for_imdb:
                        from_imdb_recomendations.append(result)
        from_imdb_recomendations = sorted(from_imdb_recomendations, key=lambda r: r["vote_average"], reverse=True)[:to_collect_from_tmdb]
        fromimdb_ids = [i["id"] for i in from_imdb_recomendations]
    return fromimdb_ids

def tmdb_recs_popular(tmdb_key, tmdb_endpoint, for_imdb, records1, fromimdb_ids):
    if len(for_imdb)==0 or len(fromimdb_ids)+len(records1)!=10:
        n = 0
        if len(for_imdb)==0:
            n = 10 - len(records1)
        
        if len(fromimdb_ids)+len(records1)!=10:
            n = 10 - (len(fromimdb_ids)+len(records1))
        
        params = {
            "api_key": tmdb_key,
            "language": "en-US",
            "page": 1
        }
        new_url = f"{tmdb_endpoint}/movie/popular"
        response = requests.get(new_url, params=params)
        results = response.json()["results"]
        top_movies = sorted(results, key=lambda x: x["popularity"], reverse=True)[:n]
        fromimdb_ids += [movie["id"] for movie in top_movies]
    return 0

def return_movie_genres(movie_id, tmdb_key):
    tmdb_movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_key}"
    tmdb_movie_response = requests.get(tmdb_movie_url)
    genres = ""
    if tmdb_movie_response.status_code == 200:
        tmdb_movie_data = tmdb_movie_response.json()
        genres = [genre["name"] for genre in tmdb_movie_data["genres"]]
    return genres

