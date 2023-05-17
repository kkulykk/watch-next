from fastapi import (
    FastAPI, 
    status
    )
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from typing import List

from .domain import WatchList, Movie
from . import service

description = """
## The API enables you to:

* Manage (list, add and delete) users' watchlists.
* Manage (list, add and delete) movies within each watchlist.
"""

tags_metadata = [
    {
        "name": "watchlists",
        "description": "Manage (list, add and delete) users' watchlists. "
        "The watchlist IDs are created automatically and are garanteed to be unique across the database.",
    },
    {
        "name": "movies",
        "description": """Manage (list, add and delete) movies within each watchlist.""",
    },
]

app = FastAPI(description=description, openapi_tags=tags_metadata)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GET   "/users/{uid}/watchlists"   
@app.get("/users/{uid}/watchlists", tags=['watchlists'])
async def list_watchlists_by_uid(uid: str) -> List[WatchList]:
    """
    List all watchlists of user with associated value of uid.
    """
    watchlists = service.list_watchlists_by_uid(uid)
    return watchlists

# POST  "/users/{uid}/watchlists?watchlist_name"
@app.post("/users/{uid}/watchlists", tags=['watchlists'])
async def create_watchlist(uid: str, watchlist_name: str):
    """
    Create watchlist with specified name for the user with specified uid
    """
    service.create_watchlist(uid, watchlist_name)

# DELETE "/users/{uid}/watchlists/{watchlist_id}"
@app.delete("/users/{uid}/watchlists/{watchlist_id}", tags=['watchlists'])
async def delete_watchlist(uid: str, watchlist_id: str):
    """
    Delete watchlist with specified id
    """
    service.delete_watchlist(uid, watchlist_id)

# GET "/users/{uid}/watchlists/{watchlist_id}/movies"
@app.get("/users/{uid}/watchlists/{watchlist_id}/movies", tags=['movies'],
responses={
    status.HTTP_200_OK: {
        "description": "Movies retrieved successfully"
    },
    status.HTTP_404_NOT_FOUND: {
        "model": str, "description": "Provided combination of uid and watchlist ID does not exist",
    }
})
async def list_movies_in_watchlist(uid: str, watchlist_id: str) -> List[Movie]:
    """
    List movies in the watchlist
    """
    try:
        movies = service.get_movies_in_watchlist(uid, watchlist_id)
        return movies
    except service.NoSuchWatchlistException:
        return Response(content="No such combination of uid and watchlist id", status_code=status.HTTP_404_NOT_FOUND)

# PUT "/users/{uid}/watchlists/{watchlist_id}/movies/{movie_id}"
@app.put("/users/{uid}/watchlists/{watchlist_id}/movies/{movie_id}", tags=['movies'])
async def add_movie_to_watchlist(uid: str, watchlist_id: str, movie_id: str):
    """
    Add movie to watchlist
    """
    service.add_movie_to_watchlist(uid, watchlist_id, movie_id)

# DELETE "/users/{uid}/watchlists/{watchlist_id}/movies/{movie_id}"
@app.delete("/users/{uid}/watchlists/{watchlist_id}/movies/{movie_id}", tags=['movies'])
async def remove_movie_from_watchlist(uid: str, watchlist_id: str, movie_id: str):
    """
    Delete movie from watchlist
    """
    service.remove_movie_from_watchlist(uid, watchlist_id, movie_id)
