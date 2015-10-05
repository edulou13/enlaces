#-*- coding: utf-8 -*-
from tornado.options import options as _options
from tornado.web import Application as _App
from os.path import (join as _join)
from . import views as _views
from .tools import (LoadConfig as _LoadConfig, url_handlers as _url_handlers, cdict as _cdict)
from .entities import db

_load_dbconf = lambda conf,flag: conf.developdb if flag else conf.productiondb
_load_slaveconf = lambda conf, flag: _cdict(host='127.0.0.1', port='8000') if not flag else conf.slaveserver

class App_Server(_App):
	def __init__(self, projdir):
		cfg = _LoadConfig(projdir).conf()
		db.bind('postgres', **_load_dbconf(cfg, _options.localdb))
		db.generate_mapping(create_tables=True)
		self.slave_server = _load_slaveconf(cfg, _options.slave)
		settings = dict(
			static_path = _join(projdir, 'statics'),
			static_hash_cache = not _options.debug,
			template_path = _join(projdir, 'templates'),
			compile_template_cache = not _options.debug,
			#compress_response = True,
			cookie_secret = 'NGM0NTRkNDIyZDRiNDg0MTU3NDE1ODNhNDU2YzYxNjM2NTcz',
			xsrf_cookies = True,
			login_url = '/login',
			server_traceback = _options.debug,
			debug = _options.debug
		)
		#print url_handlers
		super(App_Server, self).__init__(handlers=_url_handlers, **settings)