#Sash  activity

from sugar.activity import activity
from sugar.datastore import datastore
#import pygame
import logging


_logger = logging.getlogger('Sash activity')

#Search journal for title of datastore object
#and print the file path and title of DSO
ds_objects, num_objects = datastore.find({'title': 'badges_LemonadeStand'})
print "Number of Objects: " + str(num_objects)
for i in xrange(num_objects):
    print "File Path " + ds_object[i].get_file_path()
    print "Title: " + ds_object[i].metadata['title']
