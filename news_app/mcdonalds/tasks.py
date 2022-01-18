from celery import shared_task
import time

# from .models import Order

@shared_task
def hello():
    time.sleep(15)
    print("Hello, world! from from redis")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)
