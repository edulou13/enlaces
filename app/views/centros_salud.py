#-*- coding: utf-8 -*-
from pony.orm import (db_session, commit)
from json import dumps
from ..tools import (route, BaseHandler, allowedRole, cdict)
from ..entities import (Comunidad, Centro_Salud)
from ..criterias import hospitalsCrt

@route('/centros_salud/gestion')
class Gestion_Centros(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		com = Comunidad.get(**self.form2Dict)
		self.render('centros_salud/gestion.html', com=com, dumps=dumps)

@route('/centros_salud/nuevo_establecimiento')
class Nuevo_Establecimiento(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		com = Comunidad.get(**self.form2Dict)
		self.render('centros_salud/nuevo_establecimiento.html', com=com, dumps=dumps)
	@db_session
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		comunidades, prestaciones = self.get_arguments('id_com'), self.get_arguments('id_pst')
		centro = cdict(tipo=self.get_argument('tipo'), nombre=self.get_argument('nombre'), ubicado=comunidades[0])
		params = dict(hospital=centro, communities=comunidades, capabilities=prestaciones)
		self.finish(dumps(hospitalsCrt.save(**params)))

@route('/centros_salud/modificar_establecimiento')
class Modificar_Establecimiento(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		cen = Centro_Salud.get(**self.form2Dict)
		self.render('centros_salud/modificar_establecimiento.html', cen=cen, dumps=dumps)
	@db_session
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		comunidades, prestaciones = self.get_arguments('id_com'), self.get_arguments('id_pst')
		centro = cdict(tipo=self.get_argument('tipo'), nombre=self.get_argument('nombre'), id_cen=self.get_argument('id_cen'))
		params = dict(hospital=centro, communities=comunidades, capabilities=prestaciones)
		self.finish(dumps(hospitalsCrt.update(**params)))

@route('/centros_salud/eliminar_establecimiento')
class Eliminar_Establecimiento(BaseHandler):
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			cs = Centro_Salud.get(**self.form2Dict)
			if cs:
				cs.activo = False
				if not cs.comunidades.is_empty():
					cs.comunidades.clear()
				if not cs.prestaciones.is_empty():
					cs.prestaciones.clear()
				commit()
		self.finish(dumps(cs.activo))

@route('/centros_salud')
class Listar_Centros(BaseHandler):
	@db_session
	@allowedRole(u'Administrador', True)
	def get(self):
		#centros = (cs for cs in Centro_Salud.select().order_by(lambda cs:(cs.ubicado,)))
		centros = hospitalsCrt.get_all()
		self.render('centros_salud/establecimientos.html', centros=centros)