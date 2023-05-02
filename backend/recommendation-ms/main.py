import httpx
from neo4j import GraphDatabase
import requests
from fastapi import FastAPI, Header, Response, Request

app = FastAPI()

driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "mypassword"))


TMDB_API_ENDPOINT = "https://api.themoviedb.org/3"
TMDB_API_KEY = "9be9f81b03a97c8ad1b8a4a41fb190bd"

@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: int):
    try:
        records1 = []
        with driver.session() as session:
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

            result = session.run(query, {"user_id": user_id})
            lst = list(result)

            for record in lst:
                records1.append(record['other_movie_id'])

        to_collect_from_tmdb = 10-len(records1)
        for_imdb = []
        with driver.session() as session:
            query = """
            MATCH (u:User {user_id: $user_id})-[:LIKES|RATES|WATCHLIST]->(m:Movie)
            WHERE m.rating IS NOT NULL
            RETURN m.movie_id, m.genre, m.rating
            ORDER BY m.rating DESC
            LIMIT 10
            """
            result = session.run(query, {"user_id": user_id})
            for_imdb = list(result)
        
        fromimdb_ids = []
        print(fromimdb_ids)
    
        if len(for_imdb)>0:
            from_imdb_recomendations = []
            for tmdb_id in for_imdb:
                response = requests.get(f"{TMDB_API_ENDPOINT}/movie/{tmdb_id}/recommendations",
                                        params={"api_key": TMDB_API_KEY})
                if response.status_code == 200:
                    results = response.json().get("results", [])
                    for result in results:
                        if result["id"] not in records1 and result not in from_imdb_recomendations and result not in for_imdb:
                            from_imdb_recomendations.append(result)
                            print(result)
            from_imdb_recomendations = sorted(from_imdb_recomendations, key=lambda r: r["vote_average"], reverse=True)[:to_collect_from_tmdb]
            fromimdb_ids = [i["id"] for i in from_imdb_recomendations]
        if len(for_imdb)==0 or len(fromimdb_ids)+len(records1)!=10:
            n = 0
            if len(for_imdb)==0:
                n = 10 - len(records1)
            
            if len(fromimdb_ids)+len(records1)!=10:
                n = 10 - (len(fromimdb_ids)+len(records1))
            
            params = {
                "api_key": TMDB_API_KEY,
                "language": "en-US",
                "page": 1
            }
            new_url = f"{TMDB_API_ENDPOINT}/movie/popular"
            response = requests.get(new_url, params=params)
            results = response.json()["results"]
            top_movies = sorted(results, key=lambda x: x["popularity"], reverse=True)[:n]
            # return [movie["id"] for movie in top_movies]
            fromimdb_ids = [movie["id"] for movie in top_movies]

        return {'recommendations films ' : records1 + fromimdb_ids}
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
    print(user_id, movie_id, action, rating)
    tmdb_movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    tmdb_movie_response = requests.get(tmdb_movie_url)
    genres = ""
    if tmdb_movie_response.status_code == 200:
        tmdb_movie_data = tmdb_movie_response.json()
        genres = [genre["name"] for genre in tmdb_movie_data["genres"]]

    if action == 'liked':
        query = """
        MERGE (u:User {user_id: $user_id}) 
        MERGE (m:Movie {movie_id: $movie_id}) 
        CREATE (u)-[:LIKES]->(m)
        SET m.genre = $genres
        """
    elif action == 'rated':
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
    elif action == 'watched':
        query = """
        MERGE (u:User {user_id: $user_id}) 
        MERGE (m:Movie {movie_id: $movie_id}) 
        CREATE (u)-[:WATCHLIST]->(m)
        SET m.genre = $genres
        """
    else:
        return {"message": f"Invalid action: {action}"}

    with driver.session() as session:
        session.run(query, user_id=user_id, movie_id=movie_id, rating=rating, genres=genres[0])

    return {"message": "Interaction added successfully"}




# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="localhost", port=8080, log_level="debug")