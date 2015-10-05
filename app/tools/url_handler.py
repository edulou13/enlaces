#-*- coding: utf-8 -*-
from tornado.web import URLSpec as _URLSpec

url_handlers = list()

class route(object):
	def __init__(self, url, name=None):
		self.url, self.name = r'^{}$'.format(url), name
	def __call__(self, cls):
		global url_handlers
		url_handlers += [_URLSpec(self.url, cls, name=self.name) if self.name else _URLSpec(self.url, cls)]