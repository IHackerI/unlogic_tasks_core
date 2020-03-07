from datetime import datetime, timezone, timedelta
import time

def get_full_now_time(utc=False):
    base_time = datetime.utcnow() if utc else datetime.now()
    now_t_string = base_time.strftime('%Y|%m|%d|%H|%M|%S|%f|' + (time.strftime('%z') if not utc else '+0000'))
    return datetime.strptime(now_t_string, '%Y|%m|%d|%H|%M|%S|%f|%z')

def datetime_from_timestamp(timestamp):
    seconds = float(timestamp)/1000
    return datetime.fromtimestamp(seconds, tz=timezone(timedelta(milliseconds=0)))

def datetime_to_timestamp(src_val):
    return int(src_val.timestamp() * 1000)