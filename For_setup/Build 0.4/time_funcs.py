# A collection of helper functions

from datetime import datetime, timedelta


# Function from https://kite.com/python/examples/4653/datetime-round-datetime-to-any-time-interval-in-seconds
def round_time(dt=None, round_to=60):
    if dt is None:
        dt = datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds+round_to/2) // round_to * round_to
    return dt + timedelta(0, rounding-seconds, -dt.microsecond)
