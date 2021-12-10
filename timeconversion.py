"""module containing useful functions with time"""
import datetime


def current_time():
    """A function to return the current time"""
    right_now = datetime.datetime.now().strftime("%H:%M")
    return right_now


def minutes_to_seconds(minutes: str) -> int:
    """Converts minutes to seconds"""
    return int(minutes) * 60


def hours_to_minutes(hours: str) -> int:
    """Converts hours to minutes"""
    return int(hours) * 60


def hhmm_to_seconds(hhmm: str) -> int:
    """converts a digital time to an integer"""
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + minutes_to_seconds(hhmm.split(':')[1])


def time_difference(second: str) -> int:
    """Returns the difference between a given time and now is in seconds"""
    x = hhmm_to_seconds(current_time())
    y = hhmm_to_seconds(second)
    if x > y:
        return x-y
    elif y > x:
        return y-x
    else:
        return 0
