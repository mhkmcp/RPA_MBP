# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from bank_asia_scripts.Creating_info import *
from bank_asia_scripts.Parallel_process import *


@shared_task
def add():
    call = execute_the_whole_thing()
    return True


@shared_task
def mul():
    event = Event()

    dispatch = event.dispatch(event)
    return True


@shared_task
def xsum(numbers):
    return sum(numbers)