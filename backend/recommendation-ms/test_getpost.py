import requests
import sys
import time
import random

# MOVIES I ADDED TO THE NEO4J DB
# api_key = "9be9f81b03a97c8ad1b8a4a41fb190bd"
# movies_id = [603, 44826, 3042, 49638, 87101, 502781, 157336, 8392]
# Genre names for movie The Matrix with id 603: Action, Science Fiction
# Genre names for movie Hugo with id 44826: Adventure, Drama, Family
# Genre names for movie Frankenstein with id 3042: Horror, Science Fiction, TV Movie
# Genre names for movie Rhod Gilbert and The Cat That Looked Like Nicholas Lyndhurst with id 49638: Comedy
# Genre names for movie Terminator Genisys with id 87101: Science Fiction, Action, Thriller, Adventure
# Genre names for movie Sampha: Process with id 502781: Drama, Music
# Genre names for movie Interstellar with id 157336: Adventure, Drama, Science Fiction
# Genre names for movie My Neighbor Totoro with id 8392: Fantasy, Animation, Family


url = "http://localhost:8080/interactions/"

# movies_id = [603, 44826, 3042, 49638, 87101, 502781, 157336, 8392]
action_lst = ["liked", "rated", "watched"]

for movie_id in [44826, 3042, 49638, 502781]:
    for us in range(3,6):
        act = random.choice(action_lst)
        rating = None
        if act == "rated":
            rating = random.randint(1, 10)
            print(f"User {us} {act} {movie_id} as {rating} out of 10")
        else:
            print(f"User {us} {act} {movie_id}")


        payload = {
            "user_id": us,
            "movie_id": movie_id,
            "action": act,
            "rating": rating
        }

        response = requests.post(url, params=payload)


        if response.status_code != 200:
            print('Failed to add interaction')
            sys.exit(1)
        time.sleep(2)



for movie_id in [603, 87101, 157336, 8392]:
    for us in range(1,5):
        act = random.choice(action_lst)
        rating = None
        if act == "rated":
            rating = random.randint(1, 10)
            print(f"User {us} {act} {movie_id} as {rating} out of 10")
        else:
            print(f"User {us} {act} {movie_id}")
        
        payload = {
            "user_id": us,
            "movie_id": movie_id,
            "action": act,
            "rating": rating
        }

        
        response = requests.post(url, params=payload)


        if response.status_code != 200:
            print('Failed to add interaction')
            sys.exit(1)
        time.sleep(2)




