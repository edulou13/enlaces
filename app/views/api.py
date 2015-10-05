#-*- coding: utf-8 -*-
from pony.orm import (db_session,)
from json import dumps, loads
from ..tools import (route, BaseHandler, fullAsync)
from ..criterias import (personsCrt, messagesCrt, agendasCrt)

@route('/api/getsession')
class GetSession(BaseHandler):
	@fullAsync
	def get(self):
		self.set_header('Content-type', 'application/json')
		int_key, form = self.application.settings['cookie_secret'], self.form2Dict
		ext_key = form.apikey.encode('utf-8') if form.has_key('apikey') else ''
		if int_key==ext_key:
			self.finish(dumps(self.xsrf_token))
		else:
			self.finish(dumps(None))

@route('/api/feedback')
class Feeback(BaseHandler):
	@fullAsync
	def get(self):
		self.set_header('Content-type', 'application/json')
		int_key, form = self.application.settings['cookie_secret'], self.form2Dict
		ext_key = form.apikey.encode('utf-8')
		if int_key==ext_key:
			for ag in loads(form.agendas):
				agendasCrt.update_status(**ag)
			self.finish(dumps(True))
		else:
			self.finish(dumps(False))

@route('/api/getpersons')
class GetPersons(BaseHandler):
	@db_session
	@fullAsync
	def get(self):
		self.set_header('Content-type', 'application/json')
		int_key, form = self.application.settings['cookie_secret'], self.form2Dict
		ext_key = form.apikey.encode('utf-8') if form.has_key('apikey') else None
		if int_key==ext_key:
			self.finish(dumps([pr.to_dict() for pr in personsCrt.get_api()]))
		else:
			self.finish(dumps(None))

@route('/api/getmessages')
class GetMessages(BaseHandler):
	@db_session
	@fullAsync
	def get(self):
		self.set_header('Content-type', 'application/json')
		int_key, form = self.application.settings['cookie_secret'], self.form2Dict
		ext_key = form.apikey.encode('utf-8') if form.has_key('apikey') else None
		if int_key==ext_key:
			self.finish(dumps([msg.to_dict() for msg in messagesCrt.get_api()]))
		else:
			self.finish(dumps(None))

@route('/api/getagendas')
class GetAgendas(BaseHandler):
	@db_session
	@fullAsync
	def get(self):
		self.set_header('Content-type', 'application/json')
		int_key, form = self.application.settings['cookie_secret'], self.form2Dict
		ext_key = form.apikey.encode('utf-8') if form.has_key('apikey') else None
		#x_real_ip = self.request.headers.get("X-Real-IP")
		#remote_ip = self.request.remote_ip if not x_real_ip else x_real_ip
		#print remote_ip
		if int_key == ext_key:
			self.finish(dumps([ag.to_dict() for ag in agendasCrt.get_api()]))
		else:
			self.finish(dumps(None))