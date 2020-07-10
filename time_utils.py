import pytz
import datetime
from cfg import *

def localTime(zone=LOCAL_TIMEZONE):
    '''
    Returns local time based on some input TZ.
    '''
    utc = pytz.timezone("UTC").localize(datetime.datetime.utcnow())
    return utc.astimezone(pytz.timezone(LOCAL_TIMEZONE))

def UTCtoLocalTime(t, zone=LOCAL_TIMEZONE):
    '''
    Converts UTC to local time
    '''
    utc = pytz.timezone("UTC").localize(t)
    return utc.astimezone(pytz.timezone(LOCAL_TIMEZONE))