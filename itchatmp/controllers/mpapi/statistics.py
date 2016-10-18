from .common import determine_wrapper
from .mp import statistics as mpStat

'''
yiw"lpfuviwpyiw2jfu;viwp3k2d3j
'''

def user_summary(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.user_summary, None, *args)
def user_cumulate(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.user_cumulate, None, *args)
def article_summary(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.article_summary, None, *args)
def article_total(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.article_total, None, *args)
def user_read(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.user_read, None, *args)
def user_read_hour(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.user_read_hour, None, *args)
def user_share(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.user_share, None, *args)
def user_share_hour(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.user_share_hour, None, *args)
def upstream_msg(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.upstream_msg, None, *args)
def upstream_msg_hour(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.upstream_msg_hour, None, *args)
def upstream_msg_week(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.upstream_msg_week, None, *args)
def upstream_msg_month(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.upstream_msg_month, None, *args)
def upstream_msg_dist(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.upstream_msg_dist, None, *args)
def upstream_msg_dist_week(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.upstream_msg_dist_week, None, *args)
def upstream_msg_dist_month(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.upstream_msg_dist_month, None, *args)
def interface_summary(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.interface_summary, None, *args)
def interface_summary_hour(startTime, timeSection=None):
    args = (startTime,) if timeSection is None else (startTime, timeSection)
    return determine_wrapper(mpStat.interface_summary_hour, None, *args)
