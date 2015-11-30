#!/usr/bin/env python3

from gi.repository import Gtk, WebKit
import logging

UI_FILE = "browser.ui"

class Browser:

	tabs = []
	tab_contents = []
	tab_closebuttons = []
	tab_webviews = []
	tab_labels = []
	tab_titlecontainers = []

	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.btn_back = self.builder.get_object('bar-btn-back')
		self.btn_forward = self.builder.get_object('bar-btn-forward')
		self.urlbar = self.builder.get_object('bar-urlbar')

		self.tabcontainer = self.builder.get_object('tabcontainer')

		self.browser = self.builder.get_object('browser')
		self.browser.show_all()

		self.tab_append()

	def tab_new_with_glade(self, pos):
		# create new builder, see https://stackoverflow.com/questions/27737525
		builder = Gtk.Builder()
		builder.add_from_file(UI_FILE)
		self.tab_labels.insert(pos, builder.get_object('tab-title'))
		self.tab_closebuttons.insert(pos, builder.get_object('tab-close'))
		self.tab_webviews.insert(pos, WebKit.WebView())
		self.tab_webviews[pos].connect('title-changed', self.on_webview_title_changed)
		self.tab_titlecontainers.insert(pos, builder.get_object('tab-titlecontainer'))
		self.tabcontainer.insert_page(self.tab_webviews[pos], self.tab_titlecontainers[pos], pos)
		self.tabcontainer.child_set_property(self.tab_webviews[pos], 'tab-expand', True)
		self.tabcontainer.show_all()

	def tab_new(self, position):
		tab_content = Gtk.ScrolledWindow()
		tab_content.set_hexpand(True)
		tab_content.set_vexpand(True)
		tab_label = Gtk.Label(label="Empty tab")
		tab_btn_close = Gtk.Button()
		tab_btn_close.add(Gtk.Image().new_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.BUTTON))
		tab_btn_close.connect('clicked', self.on_tab_close_btn_clicked)
		tab_titlecontainer = Gtk.Box(spacing=6)
		tab_titlecontainer.pack_start(tab_label, True, True, 0)
		tab_titlecontainer.pack_start(tab_btn_close, False, False, 0)
		tab_titlecontainer.show_all()
		tab_webview = WebKit.WebView()
		tab_content.add(tab_webview)
		self.tab_contents.append(tab_content)
		self.tab_webviews.append(tab_webview)
		self.tab_labels.append(tab_label)
		self.tab_closebuttons.append(tab_btn_close)
		self.tabs.append([tab_content, tab_label, tab_webview, tab_btn_close])
		self.tabcontainer.insert_page(tab_content, tab_titlecontainer, position)
		self.tabcontainer.show_all()
		self.tabcontainer.set_current_page(position)
		tab_webview.connect("load-started", self.on_webview_load_started)
		tab_webview.connect("title-changed", self.on_webview_title_changed)
		tab_webview.connect("load-finished", self.on_webview_load_finished)

	def tab_append_next_to_self(self):
		self.tab_new_with_glade(self.tabcontainer.get_current_page())

	def tab_append(self):
		self.tab_new_with_glade(self.tabcontainer.get_n_pages())

	def tab_close_current(self):
		self.tab_close(self.tabcontainer.get_current_page())

	def tab_close(self, tab_id):
		logging.info("closing tab with id", tab_id)
		self.tabs.pop(tab_id)
		self.tabcontainer.remove_page(tab_id)

	def get_tab_by_closebutton(self):
		pass

	def on_webview_load_started(self, webview, webframe):
		self.urlbar.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY,
											'image-loading')
	def on_tab_close_clicked(self, button):
		self.tab_close(self.tab_closebuttons.index(button))

	def on_webview_load_finished(self, webview, webframe):
		self.urlbar.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY,
											None)
		if webview.get_uri() is not None:
			self.urlbar.set_text(webview.get_uri())
		self.btn_back.set_sensitive(self.tabs[self.tabcontainer.get_current_page()][2].can_go_back())
		self.btn_forward.set_sensitive(self.tabs[self.tabcontainer.get_current_page()][2].can_go_forward())

	def on_webview_title_changed(self, webview, webframe, title):
		self.tab_labels[self.tabcontainer.get_current_page()].set_text(title)

	def on_tabcontainer_switch_page(self, tabcontainer, tab_content, tab_id):
		"""if self.tabs[tab_id][2].get_uri() is not None:
			self.urlbar.set_text(self.tabs[tab_id][2].get_uri())
		else:
			self.urlbar.set_text("")
		self.btn_back.set_sensitive(self.tabs[tab_id][2].can_go_back())
		self.btn_forward.set_sensitive(self.tabs[tab_id][2].can_go_forward())"""

	def on_button_clicked(self, button):
		if button.get_stock_id() == Gtk.STOCK_GO_BACK:
			self.tabs[self.tabcontainer.get_current_page()][2].go_back()
		elif button.get_stock_id() == Gtk.STOCK_GO_FORWARD:
			self.tabs[self.tabcontainer.get_current_page()][2].go_forward()
		elif button.get_stock_id() == Gtk.STOCK_ADD:
			#self.tab_append()
			self.tab_append_next_to_self()
		elif button.get_stock_id() == Gtk.STOCK_CLOSE:
			self.tab_close_current()

	def on_urlbar_activate(self, urlbar_entry):
		entry = urlbar_entry.get_text()
		if not "http://" in entry:
			entry = "http://" + entry
		self.tab_webviews[self.tabcontainer.get_current_page()].load_uri(entry)

	def on_browser_destroy(self, window):
		Gtk.main_quit()

def main():
	browser = Browser()
	Gtk.main()

if __name__ == "__main__":
	main()