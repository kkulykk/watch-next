from pydantic import BaseModel

class WatchList(BaseModel):
    watchlist_id: str
    watchlist_name: str

class Movie(BaseModel):
    movie_id: str


