#!/usr/bin/python
from gi.repository import Gtk
import os

DEFAULT_WINDOW_SIZE = {'width': 1200, 'height': 900}


class Sash(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Sash")
        self.set_default_size(DEFAULT_WINDOW_SIZE['width'],
                              DEFAULT_WINDOW_SIZE['height'])

        # Set up all the windows
        self.window = Gtk.Grid()
        self.toolbar = Gtk.Grid(hexpand=True,
                                column_spacing=15,
                                margin_left=10)

        self.badge_window = Gtk.Grid(hexpand=True, vexpand=True)
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_border_width(10)
        self.scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

        # Connect all the windows
        self.add(self.window)
        self.window.attach(self.toolbar, 0, 0, 1, 1)
        self.window.attach(self.scrolled_window, 0, 5, 1, 3)
        self.scrolled_window.add_with_viewport(self.badge_window)

        # Display the toolbar
        self.build_toolbar()

        # Display the badges
        self.draw_badges()

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def draw_badges(self, sort_name=False, sort_date=False,
                    sort_activity=False):
        """
        Reads the user's badges and displays them in the badge_window
        """

        # Get the path of the local badges directory
        path = os.path.join(os.path.split(__file__)[0], 'badges')
        self.badges = [f for f in os.listdir(path) if os.path.isfile(
            os.path.join(path, f))]

        index = 0
        column = 0
        row = 1

        # Check if the badges need to be sorted by name
        if sort_name:
            badges = sorted(self.badges)
        else:
            badges = self.badges

        # Loop through all of the badges
        while index < len(badges):

            # Create an image and tooltip for the badge and display it
            badge = Gtk.Image(hexpand=True)
            badge.set_from_file(os.path.join(path, badges[index]))
            badge.set_tooltip_text("Name: " +
                                   badges[index].rsplit('.', 1)[0] +
                                   "\nDate Acquired: 7/21/13")
            self.badge_window.attach(badge, column, row, 1, 1)

            # If the next badge column is less than 2, increment the column
            if column < 2:
                column += 1

            # There are already 3 badges in this row, increment the row
            # and reset the column
            else:
                column = 0
                row += 1

            index += 1

        # Show all the badges on the window
        self.badge_window.show_all()

    def build_toolbar(self):
        """
        Creates and displays the toolbar
        """

        # Create a sort by name button and add a signal
        self.sort_name = Gtk.Button(label="Sort By Name")
        self.sort_name.connect("clicked", self.sort_by_name)
        self.toolbar.attach(self.sort_name, 0, 0, 1, 1)

        # Create a sort by date button and add a signal
        self.sort_date = Gtk.Button(label="Sort By Date")
        self.sort_date.connect("clicked", self.sort_by_date)
        self.toolbar.attach(self.sort_date, 1, 0, 1, 1)

        # Create a sort by activity button and add a signal
        self.sort_activity = Gtk.Button(label="Sort By Actvitiy")
        self.sort_activity.connect("clicked", self.sort_by_activity)
        self.toolbar.attach(self.sort_activity, 2, 0, 1, 1)

        # Display all toolbar items
        self.toolbar.show_all()

    def sort_by_date(self, widget):
        print "sort date"

    def sort_by_name(self, widget):
        """
        Sorts the user's badges by name
        """

        # Remove every badge that is currently being displayed
        for badge in self.badge_window.get_children():
            badge.destroy()

        # Display the user's badges sorted
        self.draw_badges(True)

    def sort_by_activity(self, widget):
        print "sort activity"


if __name__ == "__main__":
    Sash()
