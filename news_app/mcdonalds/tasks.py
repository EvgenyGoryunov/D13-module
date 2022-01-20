import instance
from celery import shared_task
import time

# from newapp.tasks import send_mail_for_sub


@shared_task
def hello():
    # задержка выполнения функции на (--) указанное время
    time.sleep(10)
    print("Hello, world! from from redis")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


@shared_task
def send_mail_for_sub_test():
    # time.sleep(10)
    print("Посылка письма, проверка111")
    # send_mail_for_sub(instance)
    print("Посылка письма, проверка222")