#Sash Activity

from sugar.activity import activity
import logging

_logger = logging.getlogger('Sash')

class SashActivity(activity.Activity):

    def __init__(self, handle):
        print "running activity init", handle
        activity.Activity.__init__(self, handle)
        print "activity running"


