import requests
import json

def create_user(email: str, username, password: str):
	r = requests.post("http://localhost:3360/create",
					  data={"email": email,
					  		"username": username,
							"hashed_password": password})
	r = json.loads(r.text)
	if "detail" in r:
		return r["detail"]
	if type(r) == str:
		return r
	return {"access_token": r["access_token"]}

def login(username: str, password: str):
	r = requests.post("http://localhost:3360/login",
					  data={"username": username,
					  		"hashed_password": password})
	r = json.loads(r.text)
	if "detail" in r:
		return r["detail"]
	if type(r) == str:
		return r
	return {"access_token": r["access_token"]}

def hello(name: str):
	return requests.get(f"http://localhost:3360/hello/{name}")

def post_to(url, json):
	r = requests.post(url, json)
	return r.text





