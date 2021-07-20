from datetime import datetime


def now_as(format):
    """Returns current date/time as a string.

    :param format: strftime() style string
    """
    now = datetime.now()
    return now.strftime(format)
