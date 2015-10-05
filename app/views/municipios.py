#-*- coding: utf-8 -*-
from pony.orm import (db_session,)
from json import dumps
from ..tools import (route, BaseHandler, allowedRole, cdict)
from ..entities import (Red_Salud, Municipio)
from ..criterias import townshipsCrt

@route(r'/municipios/gestion')
class Gestion_Municipio(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		red = Red_Salud.get(**self.form2Dict)
		self.render('municipios/gestion.html', red=red, dumps=dumps)

@route('/municipios/nuevo_municipio')
class Nuevo_Municipio(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		red = Red_Salud.get(**self.form2Dict)
		self.render('municipios/nuevo_municipio.html', red=red, dumps=dumps)
	@db_session
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		o_mup = cdict(dpto=self.get_argument('dpto'), nombre=self.get_arguments('nombre')[0])
		#o_mup.red_salud = Red_Salud.get()
		o_mup.red_salud = self.get_argument('id_red')
		comunidades = [cdict(nombre=nombre, telf=telf) for nombre, telf in zip(self.get_arguments('nombre')[1:],self.get_arguments('telf'))]
		self.finish(dumps(townshipsCrt.save(o_mup, comunidades)))

@route(r'/municipios/modificar_municipio')
class Modificar_Municipio(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		mup = Municipio.get(**self.form2Dict)
		self.render('municipios/modificar_municipio.html', mup=mup, dumps=dumps)
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(townshipsCrt.update(**self.form2Dict)))

@route('/municipios/eliminar_municipio')
class Eliminar_Municipio(BaseHandler):
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header("Content-type", "application/json")
		self.finish(dumps(townshipsCrt.delete(**self.form2Dict)))