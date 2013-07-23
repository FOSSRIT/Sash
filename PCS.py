#!/usr/bin/python
from gi.repository import Gtk
import os

DEFAULT_WINDOW_SIZE = {'width': 1200, 'height': 900}


class Sash(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Sash")
        self.set_default_size(DEFAULT_WINDOW_SIZE['width'],
                              DEFAULT_WINDOW_SIZE['height'])

        #self.options = Gtk.Box(spacing=10)
        #self.add(self.options)

        #self.sort_name = Gtk.Button(label="Sort By Name")
        #self.sort_name.connect("clicked", self.sort_by_name)
        #self.options.pack_start(self.sort_name, True, False)

        #self.sort_date = Gtk.Button(label="Sort By Date")
        #self.sort_date.connect("clicked", self.sort_by_name)

        self.grid = Gtk.Grid(hexpand=True)
        self.add(self.grid)

        path = os.path.join(os.path.split(__file__)[0], 'badges')
        badges = [f for f in os.listdir(path) if os.path.isfile(
            os.path.join(path, f))]

        index = 0
        column = 0
        row = 0

        while index < len(badges):
            badge = Gtk.Image(hexpand=True)
            badge.set_from_file(os.path.join(path, badges[index]))
            badge.set_tooltip_text("Name: " + badges[index].rsplit('.', 1)[0] +
                                   "\nDate Acquired: 7/21/13")
            self.grid.attach(badge, row, column, 1, 1)

            if row < 2:
                row += 1

            else:
                row = 0
                column += 1

            index += 1

        self.grid.show_all()

        self.connect("delete-event", Gtk.main_quit)
        self.show()
        Gtk.main()


if __name__ == "__main__":
    Sash()
