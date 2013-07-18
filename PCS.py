#Sash  activity

import pygtk
import gtk

#closes application on "delete event"
def close_application(widget, event, data = None):
    gtk.main_quit()
    return False
#makes the gtk window
def __init__(self):
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.connect("delete_event", close_application)
    window.show()
#load images
badge1 = gtk.Image()
badge1.set_from_file("images/testpic1.png")
#show images
#----background
#----badges
badge1.show()

#link to lemonade stand

#badge conditionals

#scroll bar

#main
def main():
    gtk.main()
    return 0

