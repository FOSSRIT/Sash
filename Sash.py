from gi.repository import Gtk, WebKit
from sugar3.datastore import datastore
from sugar3.activity import activity
import os
import json
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbarbox import ToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.toggletoolbutton import ToggleToolButton
from gettext import gettext as _
DEFAULT_WINDOW_SIZE = {'width': 1200, 'height': 900}


class Sash(activity.Activity):
	def __init__(self, handle):
		activity.Activity.__init__(self, handle)
		print "got here"
	
		# Email string
		self.email_text = ''

		# Filtered string
		self.search_text = ''

		# How are the badges currently being sorted
		self.current_sort = 'time'
		
		
		# Display the toolbar
		self.build_toolbar()


		#Creation of browser window
		self.browser_window = Gtk.ScrolledWindow()
		self.browser = WebKit.WebView()
		self.browser_window.add(self.browser)



		#setup badge windows
		self.badge_window = Gtk.Grid(vexpand=True, hexpand=True)
		self.scrolled_window = Gtk.ScrolledWindow()
		self.scrolled_window.set_border_width(10)
		self.scrolled_window.set_policy(
			Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

		# Connect all the windows
		self.scrolled_window.add_with_viewport(self.badge_window)


		# Load the badges
		self.load_badges()

		# Display the badges
		self.draw_badges()

		
		self.set_canvas(self.scrolled_window)
		self.show_all()

	def load_badges(self):
		"""
		Loads all of the user's badges that they have achieved.

		This allows faster sorting and searching times by creating
		a badge image and adding it to a dictionary instead of creating
		a new badge image everytime a redisplay is called.
		"""

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

		# Path to the images of the badges
		path = os.path.expanduser('~/.local/share/badges')

		# Create a dictionary of all the badge images
		self.badge_images = {}

		# Loop through all of the earned badges
		for badge in self.earned_badges.values():

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

			# Adds that badge image to the dictionary
			self.badge_images[badge['name']] = badge_image

	def draw_badges(self):
		"""
		Reads the user's badges and displays them in the badge_window
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

		# Loop through all of the badges
		for badge in badges:
			badge_image = self.badge_images[badge['name']]
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
		toolbar_box = ToolbarBox()

		#push to open badges button
		self.push_btn = ToolButton('PushToBadges')
		self.push_btn.set_tooltip(_('Push to Open Badges'))
		self.push_btn.connect("clicked", self.push_badges)
		toolbar_box.toolbar.insert(self.push_btn, -1)
		self.push_btn.show()



		#View toolbar
		self.view_toolbar = Gtk.Toolbar()

		self.sort_date_btn = ToolButton('OrganizeByDate')
		self.sort_date_btn.set_tooltip(_('Sort by Date'))
		self.sort_date_btn.connect("clicked", self.sort_badges, 'time')
		self.view_toolbar.insert(self.sort_date_btn, -1)
		self.sort_date_btn.show()

		self.sort_name_btn = ToolButton('OrganizeByName')
		self.sort_name_btn.set_tooltip(_('Sort by Name'))
		self.sort_name_btn.connect("clicked", self.sort_badges, 'name')
		self.view_toolbar.insert(self.sort_name_btn, -1)
		self.sort_name_btn.show()

		self.sort_act_btn = ToolButton('OrganizeByActivity')
		self.sort_act_btn.set_tooltip(_('Sort by Activity'))
		self.sort_act_btn.connect("clicked", self.sort_badges, 'activity')
		self.view_toolbar.insert(self.sort_act_btn, -1)
		self.sort_act_btn.show()

		# Create a button to display the current sort in ascending order
		self.descending = ToggleToolButton()
		self.descending.set_label("Descending Order")
		self.descending.connect("toggled", self.ascend_descend)
		self.view_toolbar.insert(self.descending, -1)
		self.descending.show()

		self.view_toolbar.show()

		#view toolbar button
		view_btn = ToolbarButton(
			page=self.view_toolbar,
			icon_name='toolbar-view')
		#view_btn.set_tooltip(_('View'))
		toolbar_box.toolbar.insert(view_btn, -1)
		view_btn.show()

		separator = Gtk.SeparatorToolItem()
		separator.props.draw = False
		separator.set_expand(True)
		toolbar_box.toolbar.insert(separator, -1)
		separator.show()

		#stop button
		stop_btn = StopButton(self)
		toolbar_box.toolbar.insert(stop_btn, -1)
		stop_btn.show()

		#show toolbar
		self.set_toolbar_box(toolbar_box)
		toolbar_box.show()


		"""
		# Create a search bar for badges
		self.search = Gtk.Entry()
		self.search.set_tooltip_text(
			"Search for a badge name, activity, or date")
		self.search.connect("key-release-event", self.search_badge)
		self.view_toolbar.attach(self.search, 1, 1, 3, 1)

		#Create email bar
		self.email = Gtk.Entry()
		self.email.set_tooltip_text(
			"Email")
		self.email.connect("key-release-event", self.check_email)
		self.view_toolbar.attach(self.email, 5, 0, 3, 1)

		"""
		print "test"

	def ascend_descend(self, widget):
		"""
			Toggles whether or not to display the current badges
			in ascending or descending order
		"""
		# Redisplay the badges
		self.draw_badges()

	def	push_badges(self, widget):
		"""
		Push badges should open the webview and load a dynamically created 
		webpage based on what badges are being pushed
		examples of a page can be found in the examples folder
		"""
		self.set_canvas(self.browser_window)
		self.show_all()
		path = activity.get_bundle_path()
		path = "file://" + path + "/example/test.html"
		self.browser.load_uri(path)

	def search_badge(self, widget, key):
		"""
		Search and display badges containing the search text
		"""

		# Save the searched text and draw the new set of badges
		self.search_text = widget.get_text()
		self.draw_badges()

	def check_email(self, widget, key):
		"""
		Make the email bar be saved
		"""

		# Save the text for button checking
		self.email_text = widget.get_text()

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

