#-*- coding: utf-8 -*-
from ..tools import (route, BaseHandler, fullAsync, allowedRole)
from pony.orm import (db_session,)
#from ..entities import Usuario
from ..criterias import (pregnantsCrt, pregnant_status, childrensCrt, controlsCrt, usersCrt, pregnancyWeek)
from json import dumps

@route('/', name='index')
class Index(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		if self.current_user and self.current_user.rol==u'Operador de Radio':
			self.redirect(self.reverse_url('radio'))
		else:
			assigns = dict(
				id_red = self.current_user.red_salud['id_red'] if hasattr(self.current_user, 'alcance') and self.current_user.alcance==u'2' else None,
				id_mup = self.current_user.municipio['id_mup'] if hasattr(self.current_user, 'alcance') and self.current_user.alcance==u'3' else None,
				id_cen = self.current_user.centro_salud['id_cen'] if hasattr(self.current_user, 'alcance') and self.current_user.alcance==u'4' else None)
			# print assigns
			params = dict(
				total_mujeres = pregnantsCrt.total_womens(**assigns), total_embarazos = pregnantsCrt.total_pregnants(**assigns), total_riesgos = pregnantsCrt.total_risk_pregnancies(**assigns),
				total_bebes = childrensCrt.total_childrens(**assigns), total_controles = controlsCrt.total_checked(**assigns),
				emb_status = pregnant_status, pregnancyWeek=pregnancyWeek, mujeres = pregnantsCrt.get_forDashboard(**assigns), bebes = childrensCrt.get_forDashboard(**assigns)
			)
			self.render('main/index.html', **params)

@route('/login', name='login')
class Login(BaseHandler):
	@fullAsync
	def get(self):
		self.render('main/login.html')
	@db_session
	@fullAsync
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict
		if len(form.login) and len(form.passwd):
			us = usersCrt.granted_access(form)
			if us:
				self.set_secure_cookie('user', us.to_json(), expires_days=None)#without persistence
			self.finish(dumps(True if us else False))
		else:
			self.finish(dumps(False))
		
@route('/logout', name='logout')
class Logout(BaseHandler):
	@fullAsync
	def get(self):
		self.clear_all_cookies()
		self.redirect(self.reverse_url('login'))

@route('/viewerpdf', name='viewerpdf')
class ViewerPdf(BaseHandler):
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Access-Control-Expose-Headers', 'Accept-Ranges')
		self.render('main/viewer.html')