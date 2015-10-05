#-*- coding: utf-8 -*-
from calendar import leapdays
from datetime import timedelta
from pony.orm import (db_session,)
from json import (dumps,)
from ..tools import (route, BaseHandler, allowedRole, utc, to_ddmmyy)
from ..entities import (Persona, Defuncion, Tipo)
from ..criterias import (pregnantsCrt, pregnant_status, pregnancyWeek)
from .. import deleteAgendasOnSedes

def find_pregnant(pregnant):
	tp = Tipo.get(id_tip=1)
	for tipo in pregnant.tipos:
		if tipo==tp:
			return True
	else:
		return False

def min_age():
	today = utc.now().date()
	leaps = leapdays((today.year-12), today.year)
	withoutleaps = 12 - leaps
	return today - timedelta(days=((withoutleaps*365)+(leaps*364)))

@route('/embarazadas/gestion')
class Gestion_Embarazadas(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		params = dict(embarazadas = pregnantsCrt.get_all(), emb_status=pregnant_status, pregnancyWeek=pregnancyWeek)
		self.render('embarazadas/gestion.html', **params)

@route('/embarazadas/nueva_embarazada')
class Nueva_Embarazada(BaseHandler):
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		params = dict(utc=self.utc, to_ddmmyy=to_ddmmyy, min_age=min_age)
		self.render('embarazadas/nueva_embarazada.html', **params)
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		#print self.form2Dict.keys()
		success = pregnantsCrt.save(self.form2Dict, self.current_user.id)
		self.finish(dumps(success))

@route('/embarazadas/modificar_embarazada')
class Modificar_Embarazada(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		pr = Persona.get(**self.form2Dict)
		f_locations = lambda: dict(id_com=pr.comunidad.id_com, id_mup=pr.comunidad.municipio.id_mup, id_red=pr.comunidad.municipio.red_salud.id_red) if pr.comunidad else {'id_con':None}
		checkfields = dumps(dict(is_pregnant=find_pregnant(pr), id_etn=pr.etnia.id_etn, centro_salud=pr.centro_salud.id_cen, **f_locations()))
		self.render('embarazadas/modificar_embarazada.html', pr=pr, checkfields=checkfields, to_ddmmyy=to_ddmmyy)
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = pregnantsCrt.update(**self.form2Dict)
		self.finish(dumps(flag))

@route('/embarazadas/defuncion')
class Defuncion_Embarazada(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		em = Persona.get(**self.form2Dict)
		self.render('embarazadas/defuncion.html',em=em, to_ddmmyy=to_ddmmyy)
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = pregnantsCrt.death(**self.form2Dict)
		deleteAgendasOnSedes(self, flag[1])
		self.finish(dumps(flag[0]))

@route('/embarazadas/conf_defuncion')
class ConfDefuncion_Embarazada(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		death = Defuncion.get(embarazada=self.form2Dict.id_per)
		self.render('embarazadas/conf_defuncion.html', death=death, to_ddmmyy=to_ddmmyy)
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = pregnantsCrt.confirm_death(**self.form2Dict)
		deleteAgendasOnSedes(self, flag[1])
		self.finish(dumps(flag[0]))

@route('/embarazadas/del_defuncion')
class InterrDefunction(BaseHandler):
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = pregnantsCrt.del_death(**self.form2Dict)
		self.finish(dumps(not flag))

@route('/embarazadas/eliminar')
class EliminarEmbarazada(BaseHandler):
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = pregnantsCrt.delete(**self.form2Dict)
		deleteAgendasOnSedes(self, flag[1])
		self.finish(dumps(flag[0]))