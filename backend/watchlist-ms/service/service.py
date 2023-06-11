from typing import List
from kafka import KafkaProducer
import json

from .. import repository
from ..repository import RepositorySingleton
from ..domain import WatchList, Movie

producer = KafkaProducer(
    bootstrap_servers=['kafka-server:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    api_version=(0, 10, 0)
)


class NoSuchWatchlistException(Exception):
    pass


def list_watchlists_by_uid(uid: str) -> List[WatchList]:
    repo = RepositorySingleton()
    watchlists = repo.read_watchlists_by_uid(uid)
    return watchlists


def create_watchlist(uid: str, watchlist_name: str):
    repo = RepositorySingleton()
    repo.create_watchlist(uid, watchlist_name)

def delete_watchlist(uid: str, watchlist_id: str):
    repo = RepositorySingleton()
    repo.delete_watchlist(uid, watchlist_id)


def get_movies_in_watchlist(uid: str, watchlist_id: str) -> List[Movie]:
    repo = RepositorySingleton()
    try:
        movies = repo.read_movies_from_watchlist(uid, watchlist_id)
        return movies
    except repository.NoSuchWatchlistException:
        raise NoSuchWatchlistException


def add_movie_to_watchlist(uid: str, watchlist_id: str, movie_id: str):
    repo = RepositorySingleton()
    repo.add_movie_to_watchlist(uid, watchlist_id, movie_id)

def remove_movie_from_watchlist(uid: str, watchlist_id: str, movie_id: str):
    repo = RepositorySingleton()
    repo.remove_movie_from_watchlist(uid, watchlist_id, movie_id)