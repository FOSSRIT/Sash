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

        # How are the badges currently being sorted
        self.current_sort = ''

        # Find all of the activities that award badges
        ds_objects, num_objects = datastore.find(
            {'has_badges': 'True'})

        # Create a list of tuples of all the activites
        list_activites = [(ds_object.metadata['activity'],
                           json.loads(ds_object.metadata['badge_list']))
                          for ds_object in ds_objects
                          if 'has_badges' in ds_object.metadata]

        # Creates a dictionary of earned badges and populates it
        self.earned_badges = {}
        for activity, badges in list_activites:
            for badge in badges.keys():
                self.earned_badges[badge] = {'info': badges[badge]['criteria'],
                                             'time': badges[badge]['time'],
                                             'name': badge,
                                             'bundle_id':
                                             badges[badge]['bundle_id'],
                                             'activity': activity}

        # Set up all the windows
        self.window = Gtk.Grid()
        self.toolbar = Gtk.Grid(hexpand=True,
                                column_spacing=15,
                                row_spacing=10,
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

    def draw_badges(self, sort=False, ascending=True):
        """
        Reads the user's badges and displays them in the badge_window

        :type sort: Boolean
        :param sort: Sort the badges or not (default does not)

        :type sort_by: string
        :param sort_by: Sort the badges by this key (default does nothing)
        """

        # Sort the badges a specific way
        if sort:

            # Sorts the badges in ascending order (by default)
            badges = sorted(self.earned_badges.values(),
                            key=lambda x: x[self.current_sort])
#            if self.current_sort == 'time':
#                badges = reversed(badges)

            # Sorts the badges in descending order
            if not ascending:
                badges = reversed(badges)
        else:

            badges = self.earned_badges.values()
            if not ascending:
                badges = reversed(badges)

        column = 0
        row = 1
        path = os.path.expanduser('~/.local/share/badges')

        # Loop through all of the badges
        for badge in badges:

            # Create an image and tooltip for the badge and display it
            badge_image = Gtk.Image(hexpand=True)
            badge_image.set_from_file(os.path.join(path, badge['bundle_id'],
                                      badge['name'] + '.png'))
            badge_image.set_tooltip_text("Name: " + badge['name'] +
                                         "\nDate Acquired: " +
                                         badge['time'] +
                                         "\nActivity: " +
                                         badge['activity'] +
                                         "\n\n" + badge['info'])
            self.badge_window.attach(badge_image, column, row, 1, 1)

            # If the next badge column is less than 2, increment the column
            if column < 2:
                column += 1

            # There are already 3 badges in this row, increment the row
            # and reset the column
            else:
                column = 0
                row += 1

        # Check if the user has no badges
        if len(self.earned_badges) == 0:
            message = Gtk.Label(label='You currently have no badges!' +
                                '\nGo play some games to unlock badges!',
                                hexpand=True, justify=Gtk.Justification.CENTER)
            self.badge_window.attach(message, 1, 0, 1, 1)

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

        # Create a button to display the current sort in ascending order
        self.ascending = Gtk.Button(label="Ascending")
        self.ascending.connect("clicked", self.ascending_order)
        self.toolbar.attach(self.ascending, 0, 1, 1, 1)

        # Create a button to display the current sort in descending order
        self.descending = Gtk.Button(label="Descending")
        self.descending.connect("clicked", self.descending_order)
        self.toolbar.attach(self.descending, 1, 1, 1, 1)

        # Display all toolbar items
        self.toolbar.show_all()

    def ascending_order(self, widget):

        # Remove every badge that is currently being displayed
        for badge in self.badge_window.get_children():
            badge.destroy()

        if self.current_sort == '':
            self.draw_badges(False, True)
        else:
            self.draw_badges(True)

    def descending_order(self, widget):

        # Remove every badge that is currently being displayed
        for badge in self.badge_window.get_children():
            badge.destroy()

        if self.current_sort == '':
            self.draw_badges(False, False)
        else:
            self.draw_badges(True, False)

    def sort_by_date(self, widget):
        """
        Sorts the user's badges by date acquired
        """
        # Remove every badge that is currently being displayed
        for badge in self.badge_window.get_children():
            badge.destroy()

        # Display the user's badges sorted
        self.current_sort = 'time'
        self.draw_badges(True)

    def sort_by_name(self, widget):
        """
        Sorts the user's badges by name
        """

        # Remove every badge that is currently being displayed
        for badge in self.badge_window.get_children():
            badge.destroy()

        # Display the user's badges sorted
        self.current_sort = 'name'
        self.draw_badges(True)

    def sort_by_activity(self, widget):
        """
        Sorts the user's badges by actvitiy
        """

        # Remove every badge that is currently being displayed
        for badge in self.badge_window.get_children():
            badge.destroy()

        # Display the user's badges sorted
        self.current_sort = 'activity'
        self.draw_badges(True)

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
