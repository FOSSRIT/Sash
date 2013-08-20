#!/usr/bin/python
from sugar3.activity.activity import Activity
from Sash import Sash


class SashActivity(Activity):

    def __init__(self, handle):
        print "running activity init", handle
        Activity.__init__(self, handle)
        print "activity running"

        Sash()
