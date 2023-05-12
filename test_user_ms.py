import requests
import json

def create_user(email: str, username: str, password: str):
	r = requests.post("http://localhost:3360/create",
					  data={"username": username,
						    "email": email,
							"password": password})
	r = json.loads(r.text)
	if "detail" in r:
		return r["detail"]
	if type(r) == str:
		return r
	return {"access_token": r["access_token"]}

def login(username: str, password: str):
	r = requests.post("http://localhost:3360/login",
					  data={"username": username,
					  		"password": password})
	r = json.loads(r.text)
	if "detail" in r:
		return r["detail"]
	if type(r) == str:
		return r
	return {"access_token": r["access_token"]}

def delete_account(email, username, password):
	return requests.post(f"http://localhost:3360/delete",\
						  data={"email": email,
						  	    "username": username,
								"password": password}).text

def hello(name: str):
	return requests.get(f"http://localhost:3360/hello/{name}")

def create_connection(token, friend_username):
	return requests.post(f"http://localhost:3360/friend/{token}/{friend_username}")

def remove_connection(token, friend_username):
	return requests.post(f"http://localhost:3360/unfriend/{token}/{friend_username}")

def list_connections(token):
	return requests.post(f"http://localhost:3360/friends/{token}")


