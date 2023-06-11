import httpx
from neo4j import GraphDatabase
import requests
from fastapi import FastAPI, Header, Response, Request
# from domain import domain
from services import service
from domain import domain
# from repository import repo
# from repository import *


app = FastAPI()

driver_init = domain.DriverN4j(port=7687)
driver = driver_init.driver


@app.get("/")
async def hello_world():
    return {'Hello' :1}


@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: int, num_recomendations: int = 10):
    try:
        result = await service.get_whole_recs(user_id, driver, num_recomendations)
        if result[0]:
            return {'recommendations' :  result[1]}
        else:
            return {'No recs for this user' : []}
    except requests.exceptions.JSONDecodeError:
        return {f'No such user in db': None}

@app.post("/interactions")
async def add_interaction(request: Request):
    data = await request.json()
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    action = data.get('action')
    rating = None
    if action == 'rated':
        rating = data.get('rating')
    
    
    interaction_result = await service.interaction_add(action, user_id, movie_id, driver, rating=rating)
    if interaction_result:
        return {"message": "Interaction added successfully"}

    return {"message": f"Invalid action: {action}"}


    
