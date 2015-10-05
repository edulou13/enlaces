#-*- coding: utf-8 -*-
from pony.orm import (db_session, commit)
from json import dumps
from ..tools import (route, BaseHandler, fullAsync, allowedRole)
from ..entities import (Etnia,)
from ..criterias import (ethnicsCrt,)

@route('/etnias/gestion')
class Gestion_Etnias(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		etnias = (et for et in Etnia.select())
		self.render('etnias/gestion.html', etnias=etnias, dumps=dumps)

@route('/etnias/nueva_etnia')
class Nueva_Etnia(BaseHandler):
	@allowedRole(u'Administrador')
	def get(self):
		self.render('etnias/nueva_etnia.html')
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = ethnicsCrt.save(**self.form2Dict)
		self.finish(dumps(status))

@route('/etnias/modificar_etnia')
class Modificar_Etnia(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		et = Etnia.get(**self.form2Dict)
		self.render('etnias/modificar_etnia.html', et=et)
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = ethnicsCrt.update(**self.form2Dict)
		self.finish(dumps(status))

@route('/etnias/eliminar_etnia')
class Eliminar_Etnia(BaseHandler):
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			et = Etnia.get(**self.form2Dict)
			if et:
				et.set(activo=False); commit()
		self.finish(dumps(et.activo))

@route('/etnias/disponibles')
class Etnias_Disponibles(BaseHandler):
	@fullAsync
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			etnias = dumps([dict(id_etn=et.id_etn,nombre=et.nombre) for et in Etnia.select(lambda et: et.activo)])
		self.finish(etnias)