#!/usr/bin/python
from gi.repository import Gtk
from sugar.datastore import datastore
import os
import json

DEFAULT_WINDOW_SIZE = {'width': 1200, 'height': 900}


class Sash(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Sash")
        self.set_default_size(DEFAULT_WINDOW_SIZE['width'],
                              DEFAULT_WINDOW_SIZE['height'])

        #self.remove_badges()

        # Find all of the activities that award badges
        ds_objects, num_objects = datastore.find(
            {'has_badges': 'True'})

        # Create a list of tuples of all the activites
        list_activites = [(ds_object.metadata['activity'],
                           json.loads(ds_object.metadata['badge_list']))
                          for ds_object in ds_objects]

        # Creates a dictionary of earned badges and populates it
        self.earned_badges = {}
        for activity, badges in list_activites:
            for badge in badges.keys():
                self.earned_badges[badge] = {'info': badges[badge]['criteria'],
                                             'time': badges[badge]['time'],
                                             'activity': activity}

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

        # Connects an exit function to the window
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def draw_badges(self, sort=False, sort_by=''):
        """
        Reads the user's badges and displays them in the badge_window
        """

        # Get the path of the local badges directory
        path = os.path.join(os.path.split(__file__)[0], 'badges')
        self.badges = [f for f in os.listdir(path) if os.path.isfile(
            os.path.join(path, f))]

        # Check if the badges need to be sorted by name
        if sort:
            badges = sorted(self.earned_badges.keys(),
                            key=lambda x: x[sort_by])

        # If no sort, just display them how they are
        else:
            badges = self.earned_badges.keys()

        column = 0
        row = 1
        # Loop through all of the badges
        for name in badges:

            # Create an image and tooltip for the badge and display it
            badge = Gtk.Image(hexpand=True)
            badge.set_from_file(os.path.join(path, name + '.png'))
            badge.set_tooltip_text("Name: " + name +
                                   "\nDate Acquired: " +
                                   self.earned_badges[name]['time'] +
                                   "\nActivity: " +
                                   self.earned_badges[name]['activity'] +
                                   "\n\n" + self.earned_badges[name]['info'])
            self.badge_window.attach(badge, column, row, 1, 1)

            # If the next badge column is less than 2, increment the column
            if column < 2:
                column += 1

            # There are already 3 badges in this row, increment the row
            # and reset the column
            else:
                column = 0
                row += 1

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
        """
        Sorts the user's badges by date acquired
        """
        print "sort date"

    def sort_by_name(self, widget):
        """
        Sorts the user's badges by name
        """

        # Remove every badge that is currently being displayed
        for badge in self.badge_window.get_children():
            badge.destroy()

        # Display the user's badges sorted
        self.draw_badges(True, 'name')

    def sort_by_activity(self, widget):
        """
        Sorts the user's badges by actvitiy
        """
        print "sort activity"

    def remove_badges(self):
        """
        Removes all of the user's badges from their Sash
        """

        # Find all of the activities that award badges
        ds_objects, num_objects = datastore.find(
            {'has_badges': 'True'})

        for x in range(num_objects):
            ds_objects[x].destroy()
            datastore.delete(ds_objects[x].object_id)


if __name__ == "__main__":
    Sash()
