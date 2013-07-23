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

    def draw_badges(self):

        path = os.path.join(os.path.split(__file__)[0], 'badges')
        badges = [f for f in os.listdir(path) if os.path.isfile(
            os.path.join(path, f))]

        index = 0
        column = 0
        row = 1

        while index < len(badges):
            badge = Gtk.Image(hexpand=True)
            badge.set_from_file(os.path.join(path, badges[index]))
            badge.set_tooltip_text("Name: " + badges[index].rsplit('.', 1)[0] +
                                   "\nDate Acquired: 7/21/13")
            self.badge_window.attach(badge, column, row, 1, 1)

            if column < 2:
                column += 1

            else:
                column = 0
                row += 1

            index += 1

        self.badge_window.show_all()

    def build_toolbar(self):

        self.sort_name = Gtk.Button(label="Sort By Name")
        self.sort_name.connect("clicked", self.sort_by_name)
        self.toolbar.attach(self.sort_name, 0, 0, 1, 1)

        self.sort_date = Gtk.Button(label="Sort By Date")
        self.sort_date.connect("clicked", self.sort_by_date)
        self.toolbar.attach(self.sort_date, 1, 0, 1, 1)

        self.sort_activity = Gtk.Button(label="Sort By Actvitiy")
        self.sort_activity.connect("clicked", self.sort_by_activity)
        self.toolbar.attach(self.sort_activity, 2, 0, 1, 1)

        self.toolbar.show_all()

    def sort_by_date(self, widget):
        print "sort date"

    def sort_by_name(self, widget):
        print "sort name"

    def sort_by_activity(self, widget):
        print "sort activity"


if __name__ == "__main__":
    Sash()
