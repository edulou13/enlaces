#-*- coding: utf-8 -*-
from pony.orm import db_session
from json import (dumps,)
from ..tools import (route, BaseHandler, fullAsync, allowedRole)
from ..criterias import usersCrt

@route('/usuarios/gestion')
class Gestion_Usuarios(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		usuarios = usersCrt.get_all()
		self.render('usuarios/gestion.html', usuarios=usuarios)

@route('/usuarios/nuevo_usuario')
class Nuevo_Usuario(BaseHandler):
	@allowedRole(u'Administrador')
	def get(self):
		self.render('usuarios/nuevo_usuario.html')
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(usersCrt.save(self.form2Dict)))

@route('/usuarios/modificar_usuario')
class Modificar_Usuario(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		us = usersCrt.get(**self.form2Dict)
		self.render('usuarios/modificar_usuario.html', us=us)
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(usersCrt.update(self.form2Dict)))

@route('/usuarios/eliminar_usuario')
class Eliminar_Usuario(BaseHandler):
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(usersCrt.delete(**self.form2Dict)))

@route('/usuarios/v_login')
class V_Login(BaseHandler):
	@fullAsync
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(usersCrt.v_login(**self.form2Dict)))

@route('/usuarios/v_ci')
class V_CI(BaseHandler):
	@fullAsync
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(usersCrt.v_ci(**self.form2Dict)))

@route('/usuarios/profile')
class User_Profile(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		userprofl = usersCrt.get(persona=self.current_user.id)
		self.render('usuarios/profile.html', userprofl=userprofl)
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict
		success = usersCrt.update(form)
		if success:
			self.clear_all_cookies()
			us = usersCrt.get(login=form.login)
			self.set_secure_cookie('user', us.to_json(), expires_days=None)
		self.finish(dumps(success))