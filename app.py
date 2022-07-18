import os
import platform

from flask import Flask
from celery import Celery
import redis

app = Flask(__name__)

# Redis URL config
app.config["CELERY_BROKER_URL"] = "redis://redis:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://redis:6379/0"

# Redis DB connection
redis_db = redis.Redis(
    host="redis",
    port="6379",
    db=1,
    charset="utf-8",
    decode_responses=True
)

# timer
redis_db.mset({"minute": 0, "second": 0})

# periodic tasks
celery_beat_schedule = {
    "timer_scheduler": {
        "task": "app.timer",
        "schedule": 1.0,        # run every second
    }
}

celery = Celery(app.name)
celery.conf.update(
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_url=app.config["CELERY_BROKER_URL"],
    timezone="UTC",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    beat_schedule=celery_beat_schedule,
)

@app.route("/")
def index_view():
    return "Flask-celery task scheduler!"

@app.route("/timer")
def timer_view():
    time_counter = redis_db.mget(["minute", "second"])
    return f"It runs on<br> {os.uname()}<br> node: {platform.node()}<br> for Minute: {time_counter[0]}, Second: {time_counter[1]}"

@celery.task
def timer():
    second_counter = int(redis_db.get("second")) + 1
    if second_counter >= 59:
        redis_db.set("second", 0)
        redis_db.set("minute", int(redis_db.get("minute")) + 1)
    else:
        redis_db.set("second", second_counter)

if __name__ == "__main__":
    app.run()
