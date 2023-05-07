import requests
import json

host = "http://localhost:3360"

def create_user(email: str, username: str, password: str):
	r = requests.post(f"{host}/create",
					  data={"username": username,
						    "email": email,
							"password": password})
	return r
	r = json.loads(r.text)
	if "detail" in r:
		return r["detail"]
	if type(r) == str:
		return r
	return {"access_token": r["access_token"]}

def login(username: str, password: str):
	r = requests.post(f"{host}/login",
					  data={"username": username,
					  		"password": password})
	r = json.loads(r.text)
	if "detail" in r:
		return r["detail"]
	if type(r) == str:
		return r
	return {"access_token": r["access_token"]}

def delete_account(email, username, password):
	return requests.post(f"{host}/delete",\
						  data={"email": email,
						  	    "username": username,
								"password": password}).text

def hello(name: str):
	return requests.get(f"{host}/hello/{name}")

def friend_request(username, friend_username, token):
	return requests.post(f"{host}/frequest/{username}/{friend_username}",
						json={"token": token})

def accept_request(username, friend_username, token):
	return requests.post(f"{host}/friend/{username}/{friend_username}",
						json={"token": token})

def remove_connection(username, friend_username, token):
	return requests.post(f"{host}/unfriend/{username}/{friend_username}",
						json={"token": token})

def list_connections(username, token):
	return requests.post(f"{host}/friends/{username}",
						json={"token": token})

def list_requests(username, token):
	return requests.post(f"{host}/requests/{username}",
						json={"token": token})

