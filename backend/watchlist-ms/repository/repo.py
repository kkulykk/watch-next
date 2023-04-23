from cassandra.cluster import Cluster

from functools import lru_cache
from typing import List, Union

import uuid
from ..domain import WatchList, Movie

HOST = 'watchlist-db'
PORT = 9042
KEYSPACE = 'watchlists'

class NoSuchWatchlistException(Exception):
    pass

@lru_cache(maxsize=None)
class RepositorySingleton():
    def __init__(self):
        self._cluster = Cluster([HOST], port=PORT)
        self._session = self._cluster.connect(KEYSPACE)
        
        self._read_watchlists_by_uid_statement = self._session.prepare(
            "SELECT watchlist_id, watchlist_name FROM watchlists_by_uid "
            "WHERE uid=?"
        )
        self._create_watchlist_statement = self._session.prepare(
            "INSERT INTO watchlists_by_uid(uid, watchlist_id, watchlist_name, movie_ids) "
            "VALUES (?, now(), ?, {})"
            )
        self._delete_watchlist_statement = self._session.prepare(
            "DELETE FROM watchlists_by_uid "
            "WHERE uid=? AND watchlist_id=?"
            )

        self._read_movies_from_watchlist_statement = self._session.prepare(
            "SELECT movie_ids FROM watchlists_by_uid "
            "WHERE uid=? AND watchlist_id=?"
        )
        self._add_movie_to_watchlist_statement = self._session.prepare(
            "UPDATE watchlists_by_uid "
            "SET movie_ids = movie_ids + ? "
            "WHERE uid=? AND watchlist_id=?"
            )
        self._remove_movie_from_watchlist = self._session.prepare(
            "UPDATE watchlists_by_uid "
            "SET movie_ids = movie_ids - ? "
            "WHERE uid=? AND watchlist_id=?"
        )

    # CRUD watchlists
    def read_watchlists_by_uid(self, uid: str) -> List[WatchList]:
        stmt = self._read_watchlists_by_uid_statement
        res = self._session.execute(stmt, (uid,))
        return [WatchList(watchlist_id=str(row.watchlist_id), watchlist_name=row.watchlist_name) for row in res]

    def create_watchlist(self, uid: str, watchlist_name: str):
        stmt = self._create_watchlist_statement
        self._session.execute(stmt, (uid, watchlist_name))

    def delete_watchlist(self, uid: str, watchlist_id: str):
        stmt = self._delete_watchlist_statement
        self._session.execute(stmt, (uid, uuid.UUID(watchlist_id)))

    # CRUD movies
    def read_movies_from_watchlist(self, uid: str, watchlist_id: str) -> Union[List[Movie], None]:
        stmt = self._read_movies_from_watchlist_statement
        res = self._session.execute(stmt, (uid, uuid.UUID(watchlist_id)))
        res = res.all()
        if len(res) == 0:
            raise NoSuchWatchlistException
        movie_ids = res[0].movie_ids #TODO: handle case when 0 el does not exist
        if movie_ids is None:
            return []
        return [Movie(movie_id=movie_id) for movie_id in movie_ids]

    def add_movie_to_watchlist(self, uid: str, watchlist_id: str, movie_id: str):
        stmt = self._add_movie_to_watchlist_statement
        self._session.execute(stmt, ({movie_id}, uid, uuid.UUID(watchlist_id))) #TODO: handle bad arguments

    def remove_movie_from_watchlist(self, uid: str, watchlist_id: str, movie_id: str):
        stmt = self._remove_movie_from_watchlist
        self._session.execute(stmt, ({movie_id}, uid, uuid.UUID(watchlist_id))) #TODO: handle bad arguments
