#-*- coding: utf-8 -*-
from pony.orm import (db_session,)
from json import dumps
from ..tools import (route, BaseHandler, allowedRole, cdict)
from ..entities import (Municipio, Comunidad)
from ..criterias import communitiesCrt

@route('/comunidades/gestion')
class Gestion_Comunidades(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		mup = Municipio.get(**self.form2Dict)
		self.render('comunidades/gestion.html', mup=mup, dumps=dumps)

@route('/comunidades/nueva_comunidad')
class Nueva_Comunidad(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		mup = Municipio.get(**self.form2Dict)
		self.render('comunidades/nueva_comunidad.html', mup=mup, dumps=dumps)
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		o_com = cdict(municipio=self.get_argument('id_mup'), nombre=self.get_arguments('nombre')[0], telf=self.get_argument('telf'))
		centros = [cdict(nombre=nombre,tipo=tipo) for nombre,tipo in zip(self.get_arguments('nombre')[1:],self.get_arguments('tipo'))]
		self.finish(dumps(communitiesCrt.save(o_com, centros)))

@route('/comunidades/modificar_comunidad')
class Modificar_Comunidad(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		com = Comunidad.get(**self.form2Dict)
		self.render('comunidades/modificar_comunidad.html', com=com, dumps=dumps)
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(communitiesCrt.update(**self.form2Dict)))

@route(r'/comunidades/elimininar_comunidad')
class Eliminar_Comunidad(BaseHandler):
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header("Content-type", "application/json")
		self.finish(dumps(communitiesCrt.delete(**self.form2Dict)))