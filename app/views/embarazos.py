#-*- coding: utf-8 -*-
from pony.orm import (db_session, desc)
from json import dumps
from ..tools import (route, BaseHandler, allowedRole, to_ddmmyy)
from ..entities import (Embarazo, Persona, Defuncion)
from ..criterias import (pregnanciesCrt, pregnancy_status, pregnant_status, pregnancyWeek)
from .. import deleteAgendasOnSedes

@route('/embarazos/gestion')
class Embarazos_Gestion(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		pr = Persona.get(**self.form2Dict)
		embarazos = pregnanciesCrt.get_all(pr.id_per)
		#neonatos = [neo for neo in Recien_Nacido.select(lambda neo: neo.embarazo.embarazada.id_per==pr.id_per).order_by(lambda neo: (desc(neo.creado),))]
		neonatos = [neo for emb in embarazos for neo in emb.recien_nacidos.select().order_by(lambda neo: (desc(neo.creado),))]
		params = dict(
			pr=pr, embarazos=embarazos, neonatos=neonatos,
			pregnant_status=pregnant_status, pregnancy_status=pregnancy_status,
			to_ddmmyy = to_ddmmyy, pregnancyWeek = pregnancyWeek
		)
		self.render('embarazos/gestion.html', **params)

@route('/embarazos/reg_parto')
class Reg_Parto(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		em = Embarazo.get(**self.form2Dict)
		self.render('embarazos/reg_parto.html', em=em, utc=self.utc, to_ddmmyy=to_ddmmyy)
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		success = pregnanciesCrt.childbirth(self)
		deleteAgendasOnSedes(self, success[1])
		self.finish(dumps(success[0]))

@route('/embarazos/nuevo_embarazo')
class Nuevo_Embarazo(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		params = dict(pr=Persona.get(**self.form2Dict), utc=self.utc, to_ddmmyy=to_ddmmyy)
		self.render('embarazos/nuevo_embarazo.html', **params)
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		success = pregnanciesCrt.save(**self.form2Dict)
		deleteAgendasOnSedes(self, success[1])
		self.finish(dumps(success[0]))

@route('/embarazos/reprogramar_embarazo')
class Reprogramar_Emabrazo(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		params = dict(emb=Embarazo.get(**self.form2Dict), to_ddmmyy=to_ddmmyy)
		self.render('embarazos/modificar_embarazo.html', **params)
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict
		success = pregnanciesCrt.update(**form)
		deleteAgendasOnSedes(self, success[1])
		self.finish(dumps(success[0]))

@route('/embarazos/interrumpir')
class Interrumpir_Embarazo(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		em = Embarazo.get(**self.form2Dict)
		self.render('embarazos/interrumpir.html', em=em, utc=self.utc, to_ddmmyy=to_ddmmyy)
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		success = pregnanciesCrt.interrupt(**self.form2Dict)
		deleteAgendasOnSedes(self, success[1])
		self.finish(dumps(success[0]))

@route('/embarazos/conf_interr')
class Conf_Interrupcion(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		death = Defuncion.get(embarazo=self.form2Dict.id_emb)
		self.render('embarazos/conf_interr.html', death=death, utc=self.utc, to_ddmmyy=to_ddmmyy)
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		success = pregnanciesCrt.conf_interrupt(**self.form2Dict)
		deleteAgendasOnSedes(self, success[1])
		self.finish(dumps(success[0]))

@route('/embarazos/del_interr')
class Del_Interrupcion(BaseHandler):
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		success = pregnanciesCrt.del_interrupt(**self.form2Dict)
		self.finish(dumps(not success))

@route('/embarazos/emb_riesgo')
class EmbarazoRiego(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		emb = pregnanciesCrt.get_byId(**self.form2Dict)
		self.render('embarazos/emb_riesgo.html', emb=emb)
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		success = pregnanciesCrt.risk_status(**self.form2Dict)
		self.finish(dumps(success))

@route('/embarazos/del_riesgo')
class EliminarEmbRiesgo(BaseHandler):
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		success = pregnanciesCrt.del_risk(**self.form2Dict)
		self.finish(dumps(success))