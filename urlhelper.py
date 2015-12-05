#!/usr/bin/env python3


class UrlHelper:

	def __init__(self):
		pass

	def expand_url(self, url):
		if ['http://', 'https://'] in url:
			pass
		# TODO check if list is in HTTPEverywhere list
		# if yes, expand to https, otherwise http
		# also add setting to configure that