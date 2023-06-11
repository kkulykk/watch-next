CREATE KEYSPACE watchlists WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 2} ;

USE watchlists ;

CREATE TABLE watchlists_by_uid(uid text, watchlist_id timeuuid, watchlist_name text, movie_ids set<text>, last_edit_timestamp timestamp, PRIMARY KEY (uid, watchlist_id)) ;


