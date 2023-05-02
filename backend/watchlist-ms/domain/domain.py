from pydantic import BaseModel, Field
import datetime

class WatchList(BaseModel):
    watchlist_id: str
    watchlist_name: str
    last_edit_timestamp: int = Field(description="Time of last edit in the UNIX format "
                                    "(number of seconds since Epoch)")

class Movie(BaseModel):
    movie_id: str


