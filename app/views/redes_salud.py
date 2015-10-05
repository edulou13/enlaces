#-*- coding: utf-8 -*-
from pony.orm import (db_session, commit)
from json import dumps
from ..tools import (route, BaseHandler, fullAsync, allowedRole, cdict)
from ..entities import (Red_Salud,)
from ..criterias import networksCrt

@route(r'/redes_salud/gestion')
class Gestion_RedSalud(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		redes = (rd for rd in Red_Salud.select())
		self.render('redes_salud/gestion.html', redes=redes, dumps=dumps)

@route(r'/redes_salud/nueva_red')
class Nueva_Red(BaseHandler):
	@allowedRole(u'Administrador')
	def get(self):
		self.render('redes_salud/nueva_red.html')
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		names, dptos = self.get_arguments('nombre'), self.get_arguments('dpto')
		f_mups = lambda: dict(municipios=[cdict(dpto=dpto, nombre=nombre) for dpto,nombre in zip(dptos, names[1:])])
		form = cdict(nombre=names[0], **f_mups())
		self.finish(dumps(networksCrt.save(form)))

@route(r'/redes_salud/modificar_red')
class Modificar_Red(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		red = Red_Salud.get(**self.form2Dict)
		self.render('redes_salud/modificar_red.html', red=red)
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(networksCrt.update(**self.form2Dict)))

@route('/redes_salud/eliminar_red')
class Eliminar_Red(BaseHandler):
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header("Content-type", "application/json")
		with db_session:
			red = Red_Salud.get(**self.form2Dict)
			if red:
				red.set(activo=False); commit()
		self.finish(dumps(red.activo))

@route('/redes_salud/disponibles')
class Redes_Disponibles(BaseHandler):
	@fullAsync
	def post(self):
		self.set_header('Content-type', 'application/json')
		f_redes = lambda: [dict(id_red=rd.id_red, nombre=rd.nombre, municipios=f_municipios(rd), centros=f_centros(rd)) for rd in Red_Salud.select() if rd.activo]
		f_municipios = lambda red: [dict(id_mup=mp.id_mup, nombre=mp.nombre) for mp in red.municipios if mp.activo]
		f_centros = lambda red: [dict(id_cen=cn.id_cen, nombre=cn.nombre) for mp in red.municipios for com in mp.comunidades for cn in com.centros_salud if cn.activo]
		with db_session:
			redes = f_redes()
		self.finish(dumps(redes))

@route('/redes_salud/geografia')
class Redes_Geografia(BaseHandler):
	@fullAsync
	def post(self):
		self.set_header('Content-type', 'application/json')
		f_redes = lambda: [dict(id_red=rd.id_red, nombre=rd.nombre, municipios=f_municipios(rd)) for rd in Red_Salud.select(lambda rd: rd.activo)]
		f_municipios = lambda red: [dict(id_mup=mp.id_mup, nombre=mp.nombre, comunidades=f_comunidades(mp)) for mp in red.municipios if mp.activo]
		f_comunidades = lambda municipio: [dict(id_com=cm.id_com, nombre=cm.nombre, centros_salud=f_centros(cm)) for cm in municipio.comunidades if cm.activo]
		f_centros = lambda comunidad: [dict(id_cen=cn.id_cen, nombre=cn.nombre) for cn in comunidad.atendido if cn.activo]
		with db_session:
			redes = f_redes()
			#print redes
		self.finish(dumps(redes))