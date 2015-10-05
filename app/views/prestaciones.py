#-*- coding: utf-8 -*-
from pony.orm import (db_session,)
from json import (dumps, loads)
from ..tools import (route, BaseHandler, fullAsync, allowedRole)
from ..entities import (Prestacion,)
from ..criterias import capabilitiesCrt

@route('/prestaciones/gestion')
class Gestion_Prestaciones(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		prestaciones = (pr for pr in Prestacion.select())
		self.render('prestaciones/gestion.html', prestaciones=prestaciones, dumps=dumps)

@route('/prestaciones/nueva_prestacion')
class Nueva_Prestacion(BaseHandler):
	@allowedRole(u'Administrador')
	def get(self):
		self.render('prestaciones/nueva_prestacion.html')
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = capabilitiesCrt.save(**self.form2Dict)
		self.finish(dumps(status))

@route('/prestaciones/modificar_prestacion')
class Modificar_prestacion(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		pr = Prestacion.get(**self.form2Dict)
		self.render('prestaciones/modificar_prestacion.html', pr=pr)
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = capabilitiesCrt.update(**self.form2Dict)
		self.finish(dumps(status))

@route('/prestaciones/eliminar_prestacion')
class Eliminar_Prestacion(BaseHandler):
	@allowedRole(u'Administrador')
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = capabilitiesCrt.delete(**self.form2Dict)
		self.finish(dumps(status))

@route('/prestaciones/disponibles')
class Prestaciones_Disponibles(BaseHandler):
	@db_session
	@fullAsync
	def post(self):
		self.set_header('Content-type', 'application/json')
		ids = loads(self.get_argument('prestaciones'))
		disponibles = [dict(id_pst=pr.id_pst, nombre=pr.nombre) for pr in Prestacion.select(lambda pr: pr.activo and pr.id_pst not in ids)]
		self.finish(dumps(disponibles))