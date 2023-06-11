from fastapi import FastAPI, BackgroundTasks
from app.repository import repo
import json
from datetime import datetime
import asyncio

app = FastAPI()
background_tasks = BackgroundTasks()

@app.get("/logs/{uid}")
async def log(uid: str, days=0, action=None):
    return repo.get_user_activity_by_uid(uid, days, action)

def consumer():
    for message in repo.consumer:
        record = message.value
        try:
            d = json.dumps(record)
            repo.log_user_activity(record["id"], record["action"], record["data"],\
                                   datetime.fromtimestamp(record["timestamp"]))
        except Exception as e:
            print(e)


@app.on_event("startup")
async def startup():
    background_tasks.add_task(consumer)