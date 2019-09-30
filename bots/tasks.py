# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from bank_asia_bots.Creating_info import *
from bank_asia_bots.Parallel_process import *


@shared_task
def worker_bot_process():
    # call = execute_the_whole_thing()

    print("inside worker bot")

    return True


@shared_task
def nid_bot_process():
    # event = Event()

    # dispatch = event.dispatch(event)

    print("inside nid bot")
    return True

