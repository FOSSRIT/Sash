"""
Sash Activity
 -needs to read from DSObject and journal
 -needs to display badges in some order
 -other needs?
"""
from sugar.activity import activity
from sugar.datastore import datastore
import logging

class SashActivity(activity.Activity):

    def __init__(self,handle):
        print "running activity init", handle
        activity.Activity.__init__(self, handle)
        print "activity running"

    #creates a simple textfile with filetext as the data to put into the file
    def _writetextfile(self, filename, filetext='This is some test text'):
        #create a datastore object
        file_dsobject = datastore.create()
        #write metadata
        file_dsobject.metadata['title'] = filename
        file_dsobject.metadata['mimetype'] = 'text/plain'
        #write the actual file to the data directory of the activity's root
        file_path = os.path.join(self.getactivityroot(), 'instance', filename)
        f = open(file_path, 'w')
        try:
            f.write(filetext)
        finally:
            f.close()

        #set the file_path in the datastore
        file_dsobject.set_file_path(file_path)

        datastore.write(file_dsobject)
        return file_dsobject
