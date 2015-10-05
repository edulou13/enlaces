#-*- coding: utf-8 -*-
from ..tools import (utc as _utc,)
from pony.orm import (db_session as _db_session, commit as _commit, desc as _desc, min as _min)
from ..entities import (Agenda as _Agenda, Usuario as _User)
from datetime import (timedelta as _td,)

class AgendasCriteria:
	@classmethod
	def get_api(self, start=7, end=30):
		now = _utc.now().date()
		backward, forward = (now - _td(days=start)), (now + _td(days=end))
		return _Agenda.select(lambda ag: (ag.fecha_con>=backward and ag.fecha_con<=forward) and (ag.mensaje.tipo>=1 and ag.mensaje.tipo<=5) and not(ag.sms_estado and ag.lmd_estado)).order_by(lambda ag: (ag.persona.comunidad.nombre, ag.persona.nombres, ag.persona.apellidos))
	@classmethod
	def get_byID(self, id_agd):
		return _Agenda.get(id_agd=id_agd)
	@classmethod
	def minDate(cls):
		return _min(ag.fecha_con for ag in _Agenda)
	@classmethod
	def get_all(cls):
		backward = _utc.now().date() - _td(days=30)
		return _Agenda.select(lambda ag: ag.fecha_con>=backward).order_by(lambda ag: (ag.persona.comunidad.nombre, ag.persona.nombres, ag.persona.apellidos, _desc(ag.fecha_con)))
	@classmethod
	def get_forReport(cls, id_com, start_date, end_date):
		query =_Agenda.select(lambda ag: (ag.mensaje.tipo>=1 and ag.mensaje.tipo<=5) and ag.persona.cobertura==2 and ag.persona.comunidad.id_com==id_com).order_by(lambda ag: (ag.persona.nombres, ag.persona.apellidos, ag.fecha_con))
		#query.filter(lambda ag: ag.fecha_con>=start_date and ag.modificado.date()<=end_date)
		for ag in query:
			if ag.rad_estado and (ag.fecha_con>=start_date and ag.modificado.date()<=end_date):
				yield ag
				continue
			if not ag.rad_estado and (ag.fecha_con>=start_date and ag.fecha_con<=end_date):
				yield ag
				continue
	@classmethod
	def radio_operator(cls):
		#return cls.get_api(start=15, end=15).filter(lambda ag: ag.persona.cobertura==2)
		now = _utc.now().date()
		backward, forward = (now - _td(days=15)), (now + _td(days=15))
		return _Agenda.select(lambda ag: ag.persona.cobertura==2 and (ag.fecha_con>=backward and ag.fecha_con<=forward) and (ag.mensaje.tipo>=1 and ag.mensaje.tipo<=5) and not ag.rad_estado).order_by(lambda ag: (ag.persona.comunidad.nombre, ag.persona.nombres, ag.persona.apellidos, _desc(ag.fecha_con)))
	@classmethod
	def save(self, persona, mensaje, fecha_con=None, days=0):
		try:
			with _db_session:
				if fecha_con is None:
					now = _utc.now().date().isoformat()
					ag = _Agenda(persona=persona, mensaje=mensaje, fecha_msj=now, fecha_con=now, sms_estado=True)
				else:
					fecha_msj = (fecha_con - _td(days=days)).isoformat()
					fecha_con = fecha_con.isoformat()
					ag = _Agenda(persona=persona, mensaje=mensaje, fecha_msj=fecha_msj, fecha_con=fecha_con)
				_commit()
				return True if ag else False
		except Exception, e:
			print e
			return False
	@classmethod
	def update_status(self, id_agd, sms_estado=None, lmd_estado=None, rad_estado=None, user_login=None):
		with _db_session:
			ag, user = self.get_byID(id_agd=id_agd), None
			if user_login:
				user = _User.get(login=user_login)
			if ag and sms_estado:
				ag.sms_estado = True
			if ag and lmd_estado:
				ag.lmd_estado = True
			if ag and rad_estado:
				ag.rad_estado = True
			ag.set(usuario=user); _commit()
	@classmethod
	def delete_agendas(self, obj):
		#check_date = lambda dt: True if dt>=_utc.now().date() else False
		agendas_ids = list()
		with _db_session:
			for ags in obj.agendas:
				#if not(ags.sms_estado and ags.lmd_estado) and check_date(ags.fecha_msj):
				if not(ags.sms_estado or ags.lmd_estado or ags.rad_estado):
					agendas_ids += [ags.id_agd]
					ags.delete()
			_commit()
		return agendas_ids