import requests
import json

def create_user(email: str, password: str):
	r = requests.post("http://localhost:3360/api/create",\
					  json={"email": email, "hashed_password": password})
	r = json.loads(r.text)
	if "detail" in r:
		return r["detail"]
	if type(r) == str:
		return r
	return {"access_token": r["access_token"]}

def login(email: str, password: str):
	r = requests.post("http://localhost:3360/api/login",\
					  json={"email": email, "hashed_password": password})
	r = json.loads(r.text)
	if "detail" in r:
		return r["detail"]
	if type(r) == str:
		return r
	return {"access_token": r["access_token"]}

def hello(name: str):
	return requests.get(f"http://localhost:3360/hello/{name}")


