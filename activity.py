#!/usr/bin/python
from sugar3.activity.activity import Activity
from Sash import Sash
#import logging

#_logger = logging.getlogger('Sash')


class SashActivity(Activity):

    def __init__(self, handle):
        print "running activity init", handle
        Activity.__init__(self, handle)
        print "activity running"

        Sash()
