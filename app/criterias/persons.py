#-*- coding: utf-8 -*-
from ..tools import (getLocals as _getLocals,)
from pony.orm import (db_session as _db_session, select as _select, commit as _commit)
from ..entities import (Persona as _Persona,)

class PersonsCriteria:
	@classmethod
	def v_ci(self, ci):
		try:
			with _db_session:
				return _select(pr for pr in _Persona if pr.ci==ci).exists()
		except Exception, e:
			#raise e
			return False
	@classmethod
	def v_telf(self, telf):
		try:
			with _db_session:
				return _select(pr for pr in _Persona if pr.telf==telf).exists()
		except Exception, e:
			#raise e
			return False
	@classmethod
	def get_byId(self, id_per):
		return _Persona.get(id_per=id_per)
	@classmethod
	def update(self, id_per, nombres, apellidos, telf, sexo):
		form = _getLocals(locals())
		try:
			with _db_session:
				pr = _Persona.get(id_per=id_per); del form.id_per
				pr.set(**form)
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def get_All(self, status=True):
		return _select(pr for pr in _Persona if pr.activo==status and not pr.defuncion).order_by(lambda pr: (pr.nombres, pr.apellidos))
	@classmethod
	def get_api(self):
		for pr in _Persona.select(lambda pr: not pr.contacto).order_by(lambda pr: (pr.id_per,)):
			yield pr
		for pr in _Persona.select(lambda pr: pr.contacto).order_by(lambda pr: (pr.id_per,)):
			yield pr