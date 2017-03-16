from .common import BaseController
from .mpapi.mp import statistics as mpStat

'''
yiw"lpfuviwpyiw2jfu;viwp3k2d3j
'''

class Statistics(BaseController):
    def user_summary(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.user_summary, None, *args)
    def user_cumulate(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.user_cumulate, None, *args)
    def article_summary(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.article_summary, None, *args)
    def article_total(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.article_total, None, *args)
    def user_read(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.user_read, None, *args)
    def user_read_hour(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.user_read_hour, None, *args)
    def user_share(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.user_share, None, *args)
    def user_share_hour(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.user_share_hour, None, *args)
    def upstream_msg(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.upstream_msg, None, *args)
    def upstream_msg_hour(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.upstream_msg_hour, None, *args)
    def upstream_msg_week(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.upstream_msg_week, None, *args)
    def upstream_msg_month(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.upstream_msg_month, None, *args)
    def upstream_msg_dist(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.upstream_msg_dist, None, *args)
    def upstream_msg_dist_week(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.upstream_msg_dist_week, None, *args)
    def upstream_msg_dist_month(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.upstream_msg_dist_month, None, *args)
    def interface_summary(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.interface_summary, None, *args)
    def interface_summary_hour(self, startTime, timeSection=None):
        args = (startTime,) if timeSection is None else (startTime, timeSection)
        return self.determine_wrapper(mpStat.interface_summary_hour, None, *args)
