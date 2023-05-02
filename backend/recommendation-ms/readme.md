## NEO4J DB stratup
* neo4j-desktop should be installed
* DB should be started in there with user named neo4j and password 12345678 (connection to DB through python requres these 2 params 

## Calling 
* Post example:
```
curl -X POST -H "Content-Type: application/json" -d '{"user_id": 1, "movie_id": 33, "action": "rated", "rating" : 10}' http://localhost:8080/interactions/
``` 
* Get Example:
```
curl http://localhost:8080/recommendations/1
```
(last number is used-id, which should be the same in each db)
