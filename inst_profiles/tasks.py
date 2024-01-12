from celery import shared_task
from time import sleep


@shared_task
def celery_task():
    print("Hello, celery!")
