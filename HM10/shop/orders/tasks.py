from time import sleep
from celery import shared_task


@shared_task
def send_to_console_task():
    sleep(10)
    print('Made a purchase')
