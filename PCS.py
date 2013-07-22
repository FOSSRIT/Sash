#Sash  activity
from gi.repository import Gtk

#closes application on "delete event"


#makes the gtk window and add images
def create():
    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    badge1 = Gtk.Image()
    badge1.set_from_file("images/testpic1.png")
    window.add(badge1)
    badge1.show()
    window.show_all()


def main():
    Gtk.main()
    create()

if __name__ == "__main__":
    create()
    Gtk.main()

#load images
#show images
#----background
#----badges
#link to lemonade stand
#badge conditionals
#scroll bar
