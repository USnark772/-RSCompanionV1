# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

# A collection of datetime helper functions

from datetime import datetime, timedelta


# Function from https://kite.com/python/examples/4653/datetime-round-datetime-to-any-time-interval-in-seconds
def round_time(dt=None, round_to=60):
    """ Rounds a datetime object to the nearest round_to interval. Default round_to rounds to the nearest second"""
    if dt is None:
        dt = datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds+round_to/2) // round_to * round_to
    return dt + timedelta(0, rounding-seconds, -dt.microsecond)


def get_current_time(day=False, time=False, mil=False, save=False, graph=False):
    """
    Returns a datetime string with day, time, and milliseconds options. Also available, save is formatted for when
    colons are not acceptable and graph is for the graphing utility which requires a datetime object
    """
    date_time = datetime.now()
    if day and time and mil:
        return date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    elif day and time and not mil:
        return date_time.strftime("%Y-%m-%d %H:%M:%S")
    elif day and not time and not mil:
        return date_time.strftime("%Y-%m-%d")
    elif not day and time and not mil:
        return date_time.strftime("%H:%M:%S")
    elif not day and time and mil:
        return date_time.strftime("%H:%M:%S.%f")
    elif save:
        return date_time.strftime("%Y-%m-%d-%H-%M-%S")
    elif graph:
        return date_time
