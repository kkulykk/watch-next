from pymongo import MongoClient, errors
import datetime

client = MongoClient("mongodb://localhost:27017/")

db = client["analytics-database"]

activity_collection = db["user_activity_trail"]


def log_user_activity(user_id, action, data=None):
    now = datetime.datetime.now()
    activity_action = {
        "user_id": user_id,
        "action": action,
        "data": data,
        "timestamp": now
    }
    return activity_collection.insert_one(activity_action)


def get_user_activity(user_id):
    query = {"user_id": user_id}
    results = activity_collection.find(query)

    return list(results)
