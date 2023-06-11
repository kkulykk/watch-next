from .service import (
    NoSuchWatchlistException,

    list_watchlists_by_uid,
    create_watchlist,
    delete_watchlist,

    get_movies_in_watchlist,
    remove_movie_from_watchlist,
    add_movie_to_watchlist,
)