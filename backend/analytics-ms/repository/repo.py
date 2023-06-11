from pymongo import MongoClient, errors
import datetime
from kafka import  KafkaConsumer

import os

uname = os.getenv("MONGO_INITDB_ROOT_USERNAME")
pwd = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")
n_hosts = int(os.getenv("N_MONGO_INSTANCES"))

CONNECTION_STRING = f"mongodb://{', '.join([f'localhost:270{17+i}' for i in range(n_hosts)])}"
client = MongoClient(CONNECTION_STRING)
db = client.get_database("analytics-database")
activity_collection = db["user_activity_trail"]

consumer = KafkaConsumer('activity-trail', bootstrap_servers=['kafka-server:9092'],
                         api_version=(0, 10, 1),
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

def log_user_activity(user_id, action, data=None):
    now = datetime.datetime.now()
    activity_action = {
        "user_id": user_id,
        "action": action,
        "data": data,
        "timestamp": now
    }
    return activity_collection.insert_one(activity_action)

def get_user_activity(user_id, days=0, action=None):
    query = {"user_id": user_id}
    if action:
        query["action"] = action
    if days:
        query["date"] = {"$lt": datetime.now()+datetime.timeelta(days=days),\
                         "$gte": datetime.now()}
    results = activity_collection.find(query)
    return list(results)