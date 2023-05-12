"""
test_watchlist_ms.py

Run unit tests for watchlist microservice

Usage
-----
$ docker compose -f docker-compose-watchlist-ms.yaml up -d --build
$ python3 test_watchlist_ms.py
"""

import unittest
import requests
import random
from datetime import datetime, timedelta
import time

watchlist_ms_base_url = "http://localhost:50001"

class TestStringMethods(unittest.TestCase):
    def list_watchlists_by_uid(self, uid: str):
        return requests.get(watchlist_ms_base_url + f"/users/{uid}/watchlists")
    def create_watchlist(self, uid: str, watchlist_name: str):
        params = {"watchlist_name": watchlist_name}
        return requests.post(watchlist_ms_base_url + f"/users/{uid}/watchlists", params=params)
    def delete_watchlist(self, uid: str, watchlist_id: str):
        return requests.delete(watchlist_ms_base_url + f"/users/{uid}/watchlists/{watchlist_id}")
    def list_movies_in_watchlist(self, uid: str, watchlist_id: str):
        return requests.get(watchlist_ms_base_url + f"/users/{uid}/watchlists/{watchlist_id}/movies")
    def add_movie_to_watchlist(self, uid: str, watchlist_id: str, movie_id: str):
        return requests.put(watchlist_ms_base_url + f"/users/{uid}/watchlists/{watchlist_id}/movies/{movie_id}")
    def remove_movie_from_watchlist(self, uid: str, watchlist_id: str, movie_id: str):
        return requests.delete(watchlist_ms_base_url + f"/users/{uid}/watchlists/{watchlist_id}/movies/{movie_id}")

    def test_watchlist_creation_deletion(self):
        for _ in range(10):
            uid = "0d9q23" + str(random.randint(0, 10**30))
            for _ in range(10):
                watchlist_name = "My TV-Series " + str(random.randint(0, 10**30))
                self.create_watchlist(uid, watchlist_name)
                watchlists = self.list_watchlists_by_uid(uid).json()
                self.assertEqual(watchlists[0]['watchlist_name'], watchlist_name)
                self.assertIn("watchlist_id", watchlists[0])
                self.delete_watchlist(uid, watchlists[0]['watchlist_id'])

                watchlists = self.list_watchlists_by_uid(uid).json()
                self.assertEqual(len(watchlists), 0)

    def test_movie_add_movie_remove(self):
        uid = "f04fqm" + str(random.randint(0, 10**30))
        watchlist_name = "Old-but-gold movies " + str(random.randint(0, 10**30))        
        self.create_watchlist(uid, watchlist_name)
        watchlist_id = self.list_watchlists_by_uid(uid).json()[0]['watchlist_id']

        cur_movie_ids = set()
        for _ in range(100):
            movie_id =  "sognabnm " + str(random.randint(0, 10**30))
            cur_movie_ids.add(movie_id)
            self.add_movie_to_watchlist(uid, watchlist_id, movie_id)
            received_movies = self.list_movies_in_watchlist(uid, watchlist_id).json()
            self.assertSetEqual({el['movie_id'] for el in received_movies}, cur_movie_ids)

        for _ in range(len(cur_movie_ids)):
            movie_id = cur_movie_ids.pop()
            self.remove_movie_from_watchlist(uid, watchlist_id, movie_id)
            received_movies = self.list_movies_in_watchlist(uid, watchlist_id).json()
            self.assertSetEqual({el['movie_id'] for el in received_movies}, cur_movie_ids)

        self.delete_watchlist(uid, watchlist_id)

    def test_last_edit_time(self):
        uid = "ma21kg2" + str(random.randint(0, 10**30))
        watchlist_name = "Old bw films " + str(random.randint(0, 10**30))        
        
        self.create_watchlist(uid, watchlist_name)
        watchlist_id = next(filter(lambda x: x['watchlist_name'] == watchlist_name, self.list_watchlists_by_uid(uid).json()))['watchlist_id']
        receivied_let = self.list_watchlists_by_uid(uid).json()[0]['last_edit_timestamp']
        receivied_let = datetime.fromtimestamp(receivied_let)
        self.assertLess(datetime.now() - receivied_let, timedelta(seconds=1))

        time.sleep(1.1)
        receivied_let = self.list_watchlists_by_uid(uid).json()[0]['last_edit_timestamp']
        receivied_let = datetime.fromtimestamp(receivied_let)
        self.assertGreater(datetime.now() - receivied_let, timedelta(seconds=1))

        # After adding movie
        self.add_movie_to_watchlist(uid, watchlist_id, "some_movie_id_1")
        after_add_movie_let = self.list_watchlists_by_uid(uid).json()[0]['last_edit_timestamp']
        after_add_movie_let = datetime.fromtimestamp(after_add_movie_let)
        self.assertLess(datetime.now() - after_add_movie_let, timedelta(seconds=1))

        time.sleep(1.1)
        after_add_movie_let = self.list_watchlists_by_uid(uid).json()[0]['last_edit_timestamp']
        after_add_movie_let = datetime.fromtimestamp(after_add_movie_let)
        self.assertGreater(datetime.now() - after_add_movie_let, timedelta(seconds=1))

        # After deleting movie
        self.remove_movie_from_watchlist(uid, watchlist_id, "some_movie_id_1")
        after_del_let = self.list_watchlists_by_uid(uid).json()[0]['last_edit_timestamp']
        after_del_let = datetime.fromtimestamp(after_del_let)
        self.assertLess(datetime.now() - after_del_let, timedelta(seconds=1))

        time.sleep(1.1)
        after_del_let = self.list_watchlists_by_uid(uid).json()[0]['last_edit_timestamp']
        after_del_let = datetime.fromtimestamp(after_del_let)
        self.assertGreater(datetime.now() - after_del_let, timedelta(seconds=1))

        self.delete_watchlist(uid, watchlist_id)

if __name__ == '__main__':
    unittest.main()
