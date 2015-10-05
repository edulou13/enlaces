#-*- coding: utf-8 -*-
from pony.orm import (db_session,)
from json import dumps
from ..tools import (route, BaseHandler, fullAsync, allowedRole)
from ..entities import (Tipo,)
from ..criterias import typesCrt

@route('/tipos/gestion')
class Gestion_Tipos(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		tipos = (tp for tp in Tipo.select())
		self.render('tipos/gestion.html', tipos=tipos, dumps=dumps)

@route('/tipos/nuevo_tipo')
class Nuevo_Tipo(BaseHandler):
	@allowedRole(u'Administrador')
	def get(self):
		self.render('tipos/nuevo_tipo.html')
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = typesCrt.save(**self.form2Dict)
		self.finish(dumps(status))

@route('/tipos/modificar_tipo')
class Modificar_Tipo(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		tp = Tipo.get(**self.form2Dict)
		self.render('tipos/modificar_tipo.html', tp=tp)
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = typesCrt.update(**self.form2Dict)
		self.finish(dumps(status))

@route('/tipos/disponibles')
class Tipos_Disponible(BaseHandler):
	@fullAsync
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			tipos = [dict(id_tip=tp.id_tip,nombre=tp.nombre) for tp in Tipo.select(lambda tp: tp.activo)]
		self.finish(dumps(tipos))