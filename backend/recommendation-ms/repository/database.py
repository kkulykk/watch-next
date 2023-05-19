from neo4j import GraphDatabase

# driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "mypassword"))

class DriverN4j:
    def __init__(self, port, auth_user="neo4j", auth_password="mypassword"):
        self.neo4j_url = f"bolt://neo4j:{port}"
        self.driver = GraphDatabase.driver(self.neo4j_url, auth=(f"{auth_user}", f"{auth_password}"))

TMDB_API_ENDPOINT = "https://api.themoviedb.org/3"
TMDB_API_KEY = "9be9f81b03a97c8ad1b8a4a41fb190bd"

