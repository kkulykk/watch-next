
import httpx
from neo4j import GraphDatabase
import requests
from fastapi import FastAPI, Header, Response, Request

def recs_based_onother_users(session, user_id):
    records1 = []
    with session:
        query = """
        MATCH (u:User {user_id: $user_id})-[:LIKES|RATES|WATCHLIST]->(m:Movie)
        WITH u, collect(m.genre) AS genres
        MATCH (other:Movie)
        WHERE NOT (u)-[:LIKES|RATES|WATCHLIST]->(other) AND other.genre IN genres
        WITH DISTINCT other.movie_id AS other_movie_id, other.genre AS other_genre, other.rating AS rating
        RETURN other_movie_id, other_genre, rating
        ORDER BY rating DESC
        LIMIT 5
        """
        try:
            result = session.run(query, user_id=user_id)
            lst = list(result)
        except neo4j.exceptions.ClientError:
            return {f'UID SOMETHING ERROR, uid ' : user_id}


        for record in lst:
            records1.append(record['other_movie_id'])
    
    return records1



def recs_based_onuser_watchs(session, user_id):
    for_imdb = []
    with session:
        query = """
        MATCH (u:User {user_id: $user_id})-[:LIKES|RATES|WATCHLIST]->(m:Movie)
        WHERE m.rating IS NOT NULL
        RETURN m.movie_id, m.genre, m.rating
        ORDER BY m.rating DESC
        LIMIT 10
        """
        result = session.run(query, user_id=user_id)
        for_imdb = list(result)
    return for_imdb


def add_liked_action(uid, mid, session, genres):
    query = """
        MERGE (u:User {user_id: $user_id}) 
        MERGE (m:Movie {movie_id: $movie_id}) 
        CREATE (u)-[:LIKES]->(m)
        SET m.genre = $genres
        """
    
    with session:
        session.run(query, user_id=uid, movie_id=mid, genres=genres[0])

    return query

def add_watched_action(uid, mid, session, genres):
    query = """
        MERGE (u:User {user_id: $user_id}) 
        MERGE (m:Movie {movie_id: $movie_id}) 
        CREATE (u)-[:WATCHLIST]->(m)
        SET m.genre = $genres
        """
    
    with session:
        session.run(query, user_id=uid, movie_id=mid, genres=genres[0])

    return query

def add_rated_action(uid, mid, session, rating, genres):
    query = """
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
    
    with session:
        session.run(query, user_id=uid, movie_id=mid, rating=rating, genres=genres[0])

    return query
