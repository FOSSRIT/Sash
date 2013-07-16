"""
sash Activity
"""
from sugar.activity import activity
from sugar.datastore import datastore
import pygame
import logging

_logger = logging.getlogger('Sash')

class SashActivity(activity.Activity):


    def __init__(self, handle):
        print "running activity init", handle
        activity.Activity.__init__(self, handle)
        print "activity running"

    def findDSObjects():
        ds_objects, num_objects = datastore.find({'title':
        'badges_lemonadestand'})
        print "Number of Objects: " str(num_objects)
        for i in xrange(num_objects)
        print "File Path" + ds_object[i].get_file_path()
        print "Title: " + ds_object[i].metadata['title']
