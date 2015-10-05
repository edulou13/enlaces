#-*- coding: utf-8 -*-
from ..tools import (getLocals as _getLocals, to_yymmdd as _to_yymmdd, utc as _utc)
from pony.orm import (db_session as _db_session, commit as _commit, count as _count)
from ..entities import (Recien_Nacido as _newBorn, Defuncion as _Death)
#from .controls import ControlsCriteria as _controlsCrt
from . import (networksCrt as _networksCrt, townshipsCrt as _townshipsCrt, hospitalsCrt as _hospitalsCrt)
from . import (controlsCrt as _controlsCrt, agendasCrt as _agendasCrt)
from datetime import (timedelta as _td,)

class ChildrensCriteria:
	@classmethod
	def get_allChildrens(cls, days=30):
		time_ago = _utc.now().date() - _td(days=days)
		return _newBorn.select(lambda nb: nb.embarazo.parto_inst>=time_ago)
	@classmethod
	def get_forDashboard(cls, days=30, id_red=None, id_mup=None, id_cen=None):
		time_ago = _utc.now().date() - _td(days=days)
		query = _newBorn.select(lambda nb: nb.embarazo.parto_inst>=time_ago).order_by(lambda nb: (nb.embarazo.embarazada.comunidad.nombre, nb.embarazo.parto_inst, nb.nombres, nb.apellidos))
		if id_red:
			municipios = _networksCrt.get_byId(id_red).municipios
			return query.filter(lambda nb: nb.embarazo.embarazada.comunidad.municipio in municipios)
		elif id_mup:
			comunidades = _townshipsCrt.get_byId(id_mup).comunidades
			return query.filter(lambda nb: nb.embarazo.embarazada.comunidad in comunidades)
		elif id_cen:
			comunidades = _hospitalsCrt.get_byId(id_cen).comunidades
			return query.filter(lambda nb: nb.embarazo.embarazada.comunidad in comunidades)
		else:
			return query
	@classmethod
	def total_childrens(cls, days=30, id_red=None, id_mup=None, id_cen=None):
		return _count(ch for ch in cls.get_forDashboard(days=days, id_red=id_red, id_mup=id_mup, id_cen=id_cen))
	@classmethod
	def update(cls, id_rcn, nombres, apellidos, sexo, peso):
		try:
			with _db_session:
				child = _newBorn.get(id_rcn=id_rcn)
				child.set(nombres=nombres, apellidos=apellidos, sexo=sexo, peso=peso)
				_commit()
			return True
		except Exception, e:
			raise e
			return False
	@classmethod
	def death(cls, id_rcn, fecha, f_notf, obs_notf, f_conf=None, obs_conf=None):
		deathForm = _getLocals(locals())
		deathForm.fecha, deathForm.f_notf = _to_yymmdd(fecha), _to_yymmdd(f_notf)
		try:
			agendas_ids = list()
			with _db_session:
				child = _newBorn.get(id_rcn=id_rcn)
				del deathForm.id_rcn
				if f_conf is not None:
					deathForm.f_conf = _to_yymmdd(f_conf)
					_controlsCrt.delete_controls(child)
					agendas_ids = _agendasCrt.delete_agendas(child.embarazo.embarazada)
				death = _Death(recien_nacido=child, **deathForm)
				_commit()
			return (True, agendas_ids)
		except Exception, e:
			raise e
			return (False, list())
	@classmethod
	def confirm_death(cls, id_def, f_conf, obs_conf):
		try:
			agendas_ids = list()
			with _db_session:
				death = _Death.get(id_def=id_def)
				death.set(f_conf=_to_yymmdd(f_conf), obs_conf=obs_conf)
				_controlsCrt.delete_controls(death.recien_nacido)
				agendas_ids = _agendasCrt.delete_agendas(death.recien_nacido.embarazo.embarazada)
				_commit()
			return (True, agendas_ids)
		except Exception, e:
			raise e
			return (False, list())
	@classmethod
	def delete_death(cls, id_def):
		try:
			with _db_session:
				death = _Death.get(id_def=id_def)
				death.delete()
				_commit()
			return False
		except Exception, e:
			raise e
			return True