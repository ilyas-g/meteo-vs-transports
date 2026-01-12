# api/fast.py
from fastapi import FastAPI
from redis import Redis
import time


app = FastAPI()
cache = Redis(host="redis", port=6379,db=0)


def get_count():
    count = cache.incr("count")
    if count is None:
        count = 0
    else:
        count = int(count)
    return count

# Using redis to cache a long task
@app.get("/long_task")
def long_task(id: int):
    result = cache.get(f"task_{id}")
    if result is None:
        time.sleep(5)
        print("Setting task")
        cache.set(f"task_{id}", "done")
        result = "done for first time"
    return  {"task": id, "status": result}
    

@app.get("/")
def root():
    return {"Hello": "World", "count": get_count()}