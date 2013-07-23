#!/usr/bin/python
from gi.repository import Gtk

DEFAULT_WINDOW_SIZE = {'width': 1200, 'height': 900}


class Sash(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Sash")
        self.set_default_size(DEFAULT_WINDOW_SIZE['width'],
                              DEFAULT_WINDOW_SIZE['height'])
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_border_width(10)
        self.scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        self.add(self.scrolled_window)
        self.grid = Gtk.Grid(hexpand=True)
        self.scrolled_window.add_with_viewport(self.grid)
        #display badges in the grid
        for y in range(3):
            for x in range(3):
                badge = Gtk.Image(hexpand=True)
                badge.set_from_file("badges/testpic{}.png".format(x+1))
                self.grid.attach(badge, x, y, 1, 1)

        self.scrolled_window.show_all()

        self.connect("delete-event", Gtk.main_quit)
        self.show()
        Gtk.main()


if __name__ == "__main__":
    Sash()
