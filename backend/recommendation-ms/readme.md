## Calling 
### Post example:

* liked
```
curl -X POST -H "Content-Type: application/json" -d '{"user_id": 1, "movie_id": 3042, "action": "liked"}'  http://0.0.0.0:80/interactions
``` 
* watched
```
curl -X POST -H "Content-Type: application/json" -d '{"user_id": 1, "movie_id": 3042, "action": "watched"}'  http://0.0.0.0:80/interactions
``` 
* rated (each film has it's average rating based on only our info, not the rating from TMDB)
```
curl -X POST -H "Content-Type: application/json" -d '{"user_id": 1, "movie_id": 3042, "action": "rated", "rating":6}'  http://0.0.0.0:80/interactions
``` 

You may use these movie_ids to try out commands above (valid movie ids)
```
movies_id = [603, 44826, 3042, 49638, 87101, 502781, 157336, 8392]
```

* Get Example:
```
curl http://0.0.0.0:80/recommendations/1 
```
(last number is used-id, which should be the same in each db)

```
curl http://0.0.0.0:80/recommendations/1\?num_recomendations\=25
```
default number of num_recomendations is 10, this request option shows how to set it to different numbers.

## Visualizing 

http://localhost:7474 after starting up docker and this ms visit this link to see all of the connection made (there will be none at first)