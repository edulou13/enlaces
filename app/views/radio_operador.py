#-*- coding: utf-8 -*-
from pony.orm import db_session
from json import dumps
from ..tools import route, BaseHandler, allowedRole, to_ddmmyy
from ..criterias import agendasCrt

@route('/radio_operador', name='radio')
class RadioOperador(BaseHandler):
	@db_session
	@allowedRole(u'Operador de Radio')
	def get(self):
		params = dict(
			agendas = agendasCrt.radio_operator(),
			to_ddmmyy = to_ddmmyy,
		)
		self.render('radio_operador/agendas.html', **params)
	@allowedRole(u'Operador de Radio', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		agendas, user_login = self.get_arguments('id_agd'), self.current_user.login
		for i in agendas:
			agendasCrt.update_status(id_agd=i, rad_estado=True, user_login=user_login)
		self.finish(dumps(True))