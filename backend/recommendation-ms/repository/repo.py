
# from domain.domain import Recommendation
from domain.domain import DriverN4j
import httpx
import neo4j 
import requests
from fastapi import FastAPI, Header, Response, Request
import os


class RepositorySingleton:
    def __init__(self, user_id, driver, tmdb_api_endpoint=os.environ.get("TMDB_API_ENDPOINT"), tmdb_api_key=os.environ.get("TMDB_API_KEY")):

        self.user_id = user_id
        self.session = driver.session()
        self.tmdb_key = tmdb_api_key
        self.tmdb_endpoint = tmdb_api_endpoint

        self.other_users_prefs_query = """
        MATCH (u:User {user_id: $user_id})-[:LIKES|RATES|WATCHLIST]->(m:Movie)
        WITH u, collect(m.genre) AS genres
        MATCH (other:Movie)
        WHERE NOT (u)-[:LIKES|RATES|WATCHLIST]->(other) AND other.genre IN genres
        WITH DISTINCT other.movie_id AS other_movie_id, other.genre AS other_genre, other.rating AS rating
        RETURN other_movie_id, other_genre, rating
        ORDER BY rating DESC
        LIMIT 5
        """

        self.this_user_prefs_query = """
        MATCH (u:User {user_id: $user_id})-[:LIKES|RATES|WATCHLIST]->(m:Movie)
        WITH DISTINCT m
        RETURN m.movie_id, m.genre, m.rating,
            CASE WHEN m.rating IS NULL THEN 1 ELSE 0 END AS null_rating
        ORDER BY null_rating, m.rating DESC
        LIMIT 10
        """

        self.liked_action_query = """
        MERGE (u:User {user_id: $user_id}) 
        MERGE (m:Movie {movie_id: $movie_id}) 
        CREATE (u)-[:LIKES]->(m)
        SET m.genre = $genres
        """

        self.watched_action_query = """
        MERGE (u:User {user_id: $user_id}) 
        MERGE (m:Movie {movie_id: $movie_id}) 
        CREATE (u)-[:WATCHLIST]->(m)
        SET m.genre = $genres
        """

        self.rated_action_query = """
            MERGE (u:User {user_id: $user_id})
            MERGE (m:Movie {movie_id: $movie_id})
            SET u.rating = $rating
            CREATE (u)-[:RATES {rating: $rating}]->(m)
            WITH m, AVG($rating) AS avg_rating, COUNT(*) AS num_ratings
            WITH m, avg_rating, num_ratings,
                CASE WHEN m.rating IS NOT NULL THEN (m.rating * m.number + avg_rating * num_ratings) / (m.number + num_ratings)
                    ELSE avg_rating
                END AS new_rating
            SET m.rating = new_rating,
                m.number = COALESCE(m.number, 0) + num_ratings,
                m.genre = $genres
            """
        
    def recs_based_onother_users(self):
        session = self.session 
        user_id = self.user_id
        records1 = []
        with session:
            query = self.other_users_prefs_query
            try:
                result = session.run(query, user_id=user_id)
                lst = list(result)
            except neo4j.exceptions.ClientError:
                return {f'Not valid UID ' : user_id}


            for record in lst:
                records1.append(record['other_movie_id'])
        
        return records1
    
    def recs_based_onuser_watchs(self):
        session = self.session 
        user_id = self.user_id

        for_imdb = []
        with session:
            query = self.this_user_prefs_query
            result = session.run(query, user_id=user_id)
            for_imdb = [record["m.movie_id"] for record in result]
        return for_imdb
    

    def add_liked_action(self, genres, mid):
        session = self.session 
        uid = self.user_id
        query = self.liked_action_query
    
        with session:
            session.run(query, user_id=uid, movie_id=mid, genres=genres[0])

        return query

    def add_watched_action(self, mid, genres):
        session = self.session 
        uid = self.user_id
        query = self.watched_action_query

        with session:
            session.run(query, user_id=uid, movie_id=mid, genres=genres[0])

        return query
    
    def add_rated_action(self, mid, rating, genres):
        session = self.session 
        uid = self.user_id
        query = self.rated_action_query
        
        
        with session:
            session.run(query, user_id=uid, movie_id=mid, rating=rating, genres=genres[0])

        return query



    def tmdb_recs_us1(self, for_imdb, records1, num_recomendations):
        uid = self.user_id

        fromimdb_ids = []
        to_collect_from_tmdb = num_recomendations - len(records1)
        if len(for_imdb)>0:
            from_imdb_recomendations = []
            for tmdb_id in for_imdb:
                response = requests.get(f"{self.tmdb_endpoint}/movie/{tmdb_id}/recommendations",
                                        params={"api_key": self.tmdb_key})
                if response.status_code == 200:
                    results = response.json().get("results", [])
                    for result in results:
                        if result["id"] not in records1 and result not in from_imdb_recomendations and result not in for_imdb:
                            from_imdb_recomendations.append(result)
            from_imdb_recomendations = sorted(from_imdb_recomendations, key=lambda r: r["vote_average"], reverse=True)[:to_collect_from_tmdb]
            fromimdb_ids = [i["id"] for i in from_imdb_recomendations]
        return fromimdb_ids

    def tmdb_recs_popular(self):
        
        params = {
            "api_key": self.tmdb_key,
            "language": "en-US",
            "page": 1
        }
        new_url = f"{self.tmdb_endpoint}/movie/popular"
        response = requests.get(new_url, params=params)
        results = response.json()["results"]
        top_movies = sorted(results, key=lambda x: x["popularity"], reverse=True)
        lst = [movie["id"] for movie in top_movies]

        return lst

    def return_movie_genres(self, movie_id):
        tmdb_movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.tmdb_key}"
        tmdb_movie_response = requests.get(tmdb_movie_url)
        genres = ""
        if tmdb_movie_response.status_code == 200:
            tmdb_movie_data = tmdb_movie_response.json()
            genres = [genre["name"] for genre in tmdb_movie_data["genres"]]
        return genres

