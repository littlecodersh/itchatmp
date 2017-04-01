import logging, json
from datetime import datetime, timedelta

from ..requests import requests
from itchatmp.utils import retry, encode_send_dict
from itchatmp.config import SERVER_URL
from itchatmp.content import (
    IMAGE, VOICE, VIDEO, THUMB, TEXT, NEWS, CARD)
from itchatmp.returnvalues import ReturnValue

DOC_DICT = {
    'getusersummary': ' get data of user following & unfollowing mp',
    'getusercumulate': ' get data of how many users following mp in all',
    'getarticlesummary': 'get data of daily news',
    'getarticletotal': 'get sum of all news',
    'getuserread': 'get amount of readers',
    'getuserreadhour': 'get amount of reading time',
    'getusershare': 'get amount of sharing',
    'getusersharehour': 'get amount of sharing time', 
    'getupstreammsg': 'get msg status',
    'getupstreammsghour': 'get msg status of detailed hour',
    'getupstreammsgweek': 'get msg status of weeks',
    'getupstreammsgmonth': 'get msg status of months',
    'getupstreammsgdist': 'get msg distribution',
    'getupstreammsgdistweek': 'get msg distribution of weeks',
    'getupstreammsgdistmonth': 'get msg distribution of months', 
    'getinterfacesummary': 'get interface summary',
    'getinterfacesummaryhour': 'get detailed hourly interface data',
    }

def format_time(startTime, timeSection, maxTimeSection=7):
    if not isinstance(timeSection, int) or not 1 <= timeSection <= maxTimeSection:
        return ReturnValue({'errcode': -10003, 'errmsg':
            'timeSection but be int between 1 to %s' % maxTimeSection}), None
    if hasattr(startTime, 'real'): # is number
        startTime = datetime.fromtimestamp(startTime)
    endTime = startTime + timedelta(timeSection - 1)
    return startTime.strftime("%Y-%m-%d"), endTime.strftime("%Y-%m-%d")

def fn_producer(fnName, maxTimeSection):
    def _fn_producer(startTime, timeSection=maxTimeSection, accessToken=None):
        startTime, endTime = format_time(startTime, timeSection, maxTimeSection)
        if endTime is None:
            return startTime
        def __fn_producer(startTime, endTime, accessToken=None):
            data = {'begin_date': startTime, 'end_date': endTime}
            data = encode_send_dict(data)
            r = requests.post('%s/datacube/%s?access_token=%s' % 
                (SERVER_URL, fnName, accessToken), data=data)
            def _wrap_result(result):
                result = ReturnValue(result.json())
                if 'list' in result: result['errcode'] = 0
                return result
            r._wrap_result = _wrap_result
            return r
        return __fn_producer(startTime, endTime)
    _fn_producer.__doc__ = DOC_DICT[fnName] + \
        '\n * startTime can be timestamp or datetime.datetime' + \
        ('\n * timeSection must be a int from 1 to {t},' +
            '{t} for {t} days').format(t=maxTimeSection)
    return _fn_producer

user_summary            = fn_producer('getusersummary', 7)
user_cumulate           = fn_producer('getusercumulate', 7)
article_summary         = fn_producer('getarticlesummary', 1)
article_total           = fn_producer('getarticletotal', 1)
user_read               = fn_producer('getuserread', 3)
user_read_hour          = fn_producer('getuserreadhour', 1)
user_share              = fn_producer('getusershare', 7)
user_share_hour         = fn_producer('getusersharehour', 1)
upstream_msg            = fn_producer('getupstreammsg', 7)
upstream_msg_hour       = fn_producer('getupstreammsghour', 1)
upstream_msg_week       = fn_producer('getupstreammsgweek', 30)
upstream_msg_month      = fn_producer('getupstreammsgmonth', 30)
upstream_msg_dist       = fn_producer('getupstreammsgdist', 15)
upstream_msg_dist_week  = fn_producer('getupstreammsgdistweek', 30)
upstream_msg_dist_month = fn_producer('getupstreammsgdistmonth', 30)
interface_summary       = fn_producer('getinterfacesummary', 30)
interface_summary_hour  = fn_producer('getinterfacesummaryhour', 1)
