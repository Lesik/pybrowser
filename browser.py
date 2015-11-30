#!/usr/bin/env python3

from gi.repository import Gtk, WebKit
import logging

UI_FILE = "browser.ui"

class Browser:

	tabs = []

	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.btn_back = self.builder.get_object("bar-btn-back")
		self.btn_forward = self.builder.get_object("bar-btn-forward")
		self.urlbar = self.builder.get_object("bar-urlbar")

		self.tabcontainer = self.builder.get_object("tabcontainer")

		self.browser = self.builder.get_object("browser")
		self.browser.show_all()

		self.tab_new()

	def tab_new(self):
		tab_content = Gtk.ScrolledWindow()
		tab_content.set_hexpand(True)
		tab_content.set_vexpand(True)
		tab_label = Gtk.Label("Empty tab")
		tab_webview = WebKit.WebView()
		tab_content.add(tab_webview)
		self.tabs.append([tab_content, tab_label, tab_webview])
		self.tabcontainer.append_page(tab_content, tab_label)
		self.tabcontainer.show_all()
		tab_webview.connect("title-changed", self.on_webview_title_changed)
		tab_webview.connect("load-finished", self.on_webview_load_finished)

	def tab_close_current(self):
		self.tab_close(self.tabcontainer.get_current_page())

	def tab_close(self, tab_id):
		logging.info("closing tab with id", tab_id)
		self.tabs.pop(tab_id)
		self.tabcontainer.remove_page(tab_id)

	def on_webview_load_finished(self, webview, webframe):
		self.urlbar.set_text(webview.get_uri())
		self.btn_back.set_sensitive(self.tabs[self.tabcontainer.get_current_page()][2].can_go_back())
		self.btn_forward.set_sensitive(self.tabs[self.tabcontainer.get_current_page()][2].can_go_forward())

	def on_webview_title_changed(self, webview, webframe, title):
		self.tabs[self.tabcontainer.get_current_page()][1].set_text(title)

	def on_tabcontainer_switch_page(self, tabcontainer, tab_content, tab_id):
		if self.tabs[tab_id][2].get_uri() is not None:
			self.urlbar.set_text(self.tabs[tab_id][2].get_uri())
		else:
			self.urlbar.set_text("")
		self.btn_back.set_sensitive(self.tabs[tab_id][2].can_go_back())
		self.btn_forward.set_sensitive(self.tabs[tab_id][2].can_go_forward())

	def on_button_clicked(self, button):
		if button.get_stock_id() == Gtk.STOCK_GO_BACK:
			self.tabs[self.tabcontainer.get_current_page()][2].go_back()
		elif button.get_stock_id() == Gtk.STOCK_GO_FORWARD:
			self.tabs[self.tabcontainer.get_current_page()][2].go_forward()
		elif button.get_stock_id() == Gtk.STOCK_ADD:
			print("lel")
			self.tab_new()
		elif button.get_stock_id() == Gtk.STOCK_CLOSE:
			self.tab_close_current()

	def on_urlbar_activate(self, urlbar_entry):
		entry = urlbar_entry.get_text()
		if not "http://" in entry:
			entry = "http://" + entry
		self.tabs[self.tabcontainer.get_current_page()][2].load_uri(entry)

	def on_browser_destroy(self, window):
		Gtk.main_quit()

def main():
	browser = Browser()
	Gtk.main()

if __name__ == "__main__":
	main()