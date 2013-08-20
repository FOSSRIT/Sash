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

        # Filtered string
        self.search_text = ''

        # How are the badges currently being sorted
        self.current_sort = None

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

        self.badge_window = Gtk.Grid(
            vexpand=True,
            hexpand=True,
            column_spacing=120,
            margin_left=35)

        self.badge_background = Gtk.Grid()
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_border_width(10)
        self.scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

        # Connect all the windows
        self.add(self.window)
        self.window.attach(self.toolbar, 0, 0, 1, 1)
        self.window.attach(self.scrolled_window, 0, 5, 1, 3)
        self.badge_background.attach(self.badge_window, 0, 0, 1, 3)
        self.scrolled_window.add_with_viewport(self.badge_background)

        # Display the toolbar
        self.build_toolbar()

        # Display the badges
        self.draw_badges()

        # Connects an exit function to the window
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def draw_badges(self):
        """
        Reads the user's badges and displays them in the badge_window

        :type sort: Boolean
        :param sort: Sort the badges or not (default does not)

        :type sort_by: string
        """

        # Clear the current screen of badges
        for badge in self.badge_window.get_children():
            badge.destroy()

        badges = []

        # Add badges that contain the specific search text
        for badge in self.earned_badges.values():
            if self.search_text.lower() in (
                    badge['name'].lower() +
                    badge['activity'].lower() +
                    badge['time']):
                badges.append(badge)

        # Sort the badges a specific way
        if self.current_sort is not None:

            # Sorts the badges in ascending order (by default)
            badges = sorted(badges,
                            key=lambda x: x[self.current_sort])

        # Display the badges in descending order if the button is toggled
        if self.descending.get_active():
            badges = reversed(badges)

        column = 0
        row = 1
        path = os.path.expanduser('~/.local/share/badges')

        # Loop through all of the badges
        for badge in badges:

            # Create an image and tooltip for the badge and display it
            badge_image = Gtk.Image()
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

        # Create a container for the radio buttons
        self.sort_box = Gtk.Box(spacing=6)
        self.toolbar.attach(self.sort_box, 0, 0, 3, 1)

        # Create a sort by nothing button and add a signal
        self.sort_none = Gtk.RadioButton(None, "None")
        self.sort_none.connect("toggled", self.sort_badges, None)
        self.sort_box.pack_start(self.sort_none, False, False, 0)

        # Create a sort by name button and add a signal
        self.sort_name = Gtk.RadioButton.new_from_widget(self.sort_none)
        self.sort_name.set_label("Sort By Name")
        self.sort_name.connect("toggled", self.sort_badges, 'name')
        self.sort_box.pack_start(self.sort_name, False, False, 0)

        # Create a sort by date button and add a signal
        self.sort_date = Gtk.RadioButton.new_from_widget(self.sort_none)
        self.sort_date.set_label("Sort By Date")
        self.sort_date.connect("toggled", self.sort_badges, 'time')
        self.sort_box.pack_start(self.sort_date, False, False, 0)

        # Create a sort by activity button and add a signal
        self.sort_activity = Gtk.RadioButton.new_from_widget(self.sort_none)
        self.sort_activity.set_label("Sort By Actvitiy")
        self.sort_activity.connect("toggled", self.sort_badges, 'activity')
        self.sort_box.pack_start(self.sort_activity, False, False, 0)

        # Create a button to display the current sort in ascending order
        self.descending = Gtk.ToggleButton(label="Descending Order")
        self.descending.connect("toggled", self.ascend_descend)
        self.toolbar.attach(self.descending, 0, 1, 1, 1)

        # Create a search bar for badges
        self.search = Gtk.Entry()
        self.search.set_tooltip_text(
            "Search for a badge name, activity, or date")
        self.search.connect("key-release-event", self.search_badge)
        self.toolbar.attach(self.search, 1, 1, 2, 1)

        # Display all toolbar items
        self.toolbar.show_all()

    def ascend_descend(self, widget):
        """
        Toggles whether or not to display the current badges
        in ascending or descending order
        """

        # Redisplay the badges
        self.draw_badges()

    def search_badge(self, widget, key):
        """
        Search and display badges containing the search text
        """

        # Save the searched text and draw the new set of badges
        self.search_text = widget.get_text()
        self.draw_badges()

    def sort_badges(self, widget, sort_type):
        """
        Sort and display the badges by the sort type provided
        """

        # Save the sort type and draw the new set of badges
        self.current_sort = sort_type
        self.draw_badges()

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
