#-*- coding: utf-8 -*-
from datetime import timedelta as _timedelta
from pony.orm import (db_session as _db_session, commit as _commit, flush as _flush, desc as _desc)
from ..entities import (Embarazo as _Embarazo, Control as _Control, Recien_Nacido as _NewBorn, Persona as _Persona, Defuncion as _Defuncion)
from ..tools import (to_date as _to_date, to_yymmdd as _to_yymmdd, PreNatal as _PreNatal, PrePromotional as _PrePromotional, PostNatal as _PostNatal, Interruption as _Interruption)
from . import (controlsCrt as _controlsCrt, messagesCrt as _messagesCrt, agendasCrt as _agendasCrt)

def pregnancy_status(prg):
	pregnant = prg.embarazada
	if not prg.activo and not(prg.interrupcion):
		return (0, u'Embarazo Culminado')
	if pregnant.activo and not pregnant.defuncion and prg and not prg.interrupcion and not prg.riesgo:
		return (1, u'Gestando')
	elif pregnant.activo and not pregnant.defuncion and prg and not prg.interrupcion and prg.riesgo:
		return (2, u'Embarazo de Riesgo')
	elif pregnant.activo and not pregnant.defuncion and prg and prg.interrupcion and not prg.interrupcion.f_conf:
		return (3, u'Advertencia')#Interruption
	elif pregnant.activo and pregnant.defuncion and not pregnant.defuncion.f_conf and prg and prg.interrupcion and not prg.interrupcion.f_conf:
		return (4, u'Advertencia')#Defunction
	elif prg and prg.interrupcion and prg.interrupcion.f_conf:
		return (5, u'Embarazo Interrumpido')
	else:
		return (-1, '')

class PregnanciesCriteria:
	@classmethod
	def get_byId(cls, id_emb):
		return _Embarazo.get(id_emb=id_emb)
	@classmethod
	def get_all(self, id_per):
		return _Embarazo.select(lambda emb: emb.embarazada.id_per==id_per).order_by(lambda emb: (_desc(emb.creado),))
	@classmethod
	def save(self, id_per, parto_prob):
		try:
			parto_prob = _to_yymmdd(parto_prob)
			pp = _to_date(parto_prob) - _timedelta(days=280)
			#print 'origin: {}'.format(pp)
			ctrls = _PreNatal(pp.year, pp.month, pp.day)
			if not ctrls.check_range():
				return (False, list())
			promos = _PrePromotional(pp.year, pp.month, pp.day).controls_dates()
			agendas_ids = list()
			with _db_session:
				pregnant = _Persona.get(id_per=id_per)
				pregnancy = _Embarazo(embarazada=pregnant, parto_prob=parto_prob)
				_controlsCrt.delete_controls(pregnancy)
				agendas_ids = _agendasCrt.delete_agendas(pregnant)
				pregnancy.controles += [_Control(embarazo=pregnancy, nro_con=ctrl[0], fecha_con=ctrl[1]) for ctrl in ctrls.controls_dates()]
				_flush()
				for cn in pregnancy.controles:
					msg = _messagesCrt.get_byNumbControl(nro_control=cn.nro_con)
					_agendasCrt.save(persona=pregnant, mensaje=msg, fecha_con=cn.fecha_con, days=7)
				for cn in promos:
					msg = _messagesCrt.get_byNumbControl(nro_control=cn[0], tipo=3)
					_agendasCrt.save(persona=pregnant, mensaje=msg, fecha_con=cn[1])
				_commit()
			return (True, agendas_ids)
		# except AssertionError:
		# 	return (False, list())
		except Exception, e:
			#raise e
			print e
			return (False, list())
	@classmethod
	def update(cls, id_emb, parto_prob):
		try:
			parto_prob = _to_yymmdd(parto_prob)
			pp = _to_date(parto_prob) - _timedelta(days=280)
			ctrls = _PreNatal(pp.year, pp.month, pp.day)
			if not ctrls.check_range():
				return (False, list())
			promos = _PrePromotional(pp.year, pp.month, pp.day).controls_dates()
			agendas_ids = list()
			with _db_session:
				pregnancy = cls.get_byId(id_emb=id_emb)
				pregnancy.set(parto_prob=parto_prob)
				_controlsCrt.delete_controls(pregnancy)
				agendas_ids = _agendasCrt.delete_agendas(pregnancy.embarazada)
				pregnancy.controles += [_Control(embarazo=pregnancy, nro_con=ctrl[0], fecha_con=ctrl[1]) for ctrl in ctrls.controls_dates()]
				_flush()
				for cn in pregnancy.controles:
					msg = _messagesCrt.get_byNumbControl(nro_control=cn.nro_con)
					_agendasCrt.save(persona=pregnancy.embarazada, mensaje=msg, fecha_con=cn.fecha_con, days=7)
				for cn in promos:
					msg = _messagesCrt.get_byNumbControl(nro_control=cn[0], tipo=3)
					_agendasCrt.save(persona=pregnancy.embarazada, mensaje=msg, fecha_con=cn[1])
				_commit()
			return (True, agendas_ids)
		except Exception, e:
			#raise e
			print 'Error: {}'.format(e)
			return (False, list())
	@classmethod
	def childbirth(self, obj):
		try:
			pinst = _to_date(_to_yymmdd(obj.get_argument('parto_inst')))
			ctrls = _PostNatal(pinst.year, pinst.month, pinst.day).controls_dates()
			#f_emb = lambda: dict(parto_inst=obj.get_argument('parto_inst'),tipo=obj.get_argument('tipo'),observacion=obj.get_argument('observacion'))
			f_emb = lambda: dict(parto_inst=_to_yymmdd(obj.get_argument('parto_inst')),tipo=obj.get_argument('tipo'))
			pesos, nombres, apellidos = obj.get_arguments('peso'), obj.get_arguments('nombres'), obj.get_arguments('apellidos')
			sexos = [obj.get_argument('sexo{}'.format(s)) for s in xrange(len(nombres))] if len(nombres)>1 else [obj.get_argument('sexo0')]
			agendas_ids = list()
			with _db_session:
				em = _Embarazo.get(id_emb=obj.get_argument('id_emb'))
				em.set(activo=False, **f_emb()); _flush()
				_controlsCrt.delete_controls(em)
				agendas_ids = _agendasCrt.delete_agendas(em.embarazada)
				controls = lambda: [_Control(tipo=u'Post-Natal', nro_con=ctrl[0], fecha_con=ctrl[1]) for ctrl in ctrls]
				em.recien_nacidos += [_NewBorn(embarazo=em,peso=nb[0],sexo=nb[1],nombres=nb[2],apellidos=nb[3],controles=controls()) for nb in zip(pesos,sexos,nombres,apellidos)]
				_flush()
				for rn in em.recien_nacidos:
					for cn in rn.controles:
						msg = _messagesCrt.get_byNumbControl(nro_control=cn.nro_con, tipo=2)
						_agendasCrt.save(persona=em.embarazada, mensaje=msg, fecha_con=cn.fecha_con)
					break
				#em.controles += [_Control(embarazo=em, tipo=u'Post-Natal', nro_con=ctrl[0], fecha_con=ctrl[1]) for ctrl in ctrls.controls_dates()]
				_commit()
			return (True, agendas_ids)
		except Exception, e:
			#raise e
			print e
			return (False, list())
	@classmethod
	def interrupt(self, id_emb, fecha, f_notf, obs_notf, f_conf=None, obs_conf=None):
		f_interr = lambda: dict(fecha=_to_yymmdd(fecha), f_notf=_to_yymmdd(f_notf), obs_notf=obs_notf.upper()) if f_conf is None else dict(fecha=_to_yymmdd(fecha), f_notf=_to_yymmdd(f_notf), obs_notf=obs_notf.upper(), f_conf=_to_yymmdd(f_conf), obs_conf=obs_conf.upper())
		try:
			agendas_ids = list()
			with _db_session:
				em = _Embarazo.get(id_emb=id_emb)
				if f_conf:
					_controlsCrt.delete_controls(em)
					em.activo = False
					if not em.embarazada.agendas.is_empty():
						agendas_ids = _agendasCrt.delete_agendas(em.embarazada)
					dt = _to_date(_to_yymmdd(fecha))
					for cn in _Interruption(dt.year, dt.month, dt.day).controls_dates():
						msg = _messagesCrt.get_byNumbControl(nro_control=cn[0], tipo=5)
						_agendasCrt.save(persona=em.embarazada, mensaje=msg, fecha_con=cn[1])
				_Defuncion(embarazo=em, **f_interr()); _commit()
			return (True, agendas_ids)
		except Exception, e:
			#raise e
			print e
			return (False, list())
	@classmethod
	def conf_interrupt(self, id_def, f_conf, obs_conf):
		try:
			f_conf = _to_yymmdd(f_conf)
			agendas_ids = list()
			with _db_session:
				interr = _Defuncion.get(id_def=id_def)
				interr.set(f_conf=f_conf, obs_conf=obs_conf.upper())
				interr.embarazo.activo = False
				_controlsCrt.delete_controls(interr.embarazo)
				if not interr.embarazo.embarazada.agendas.is_empty():
					agendas_ids = _agendasCrt.delete_agendas(interr.embarazo.embarazada)
				dt = _to_date(f_conf)
				for cn in _Interruption(dt.year, dt.month, dt.day).controls_dates():
					msg = _messagesCrt.get_byNumbControl(nro_control=cn[0], tipo=5)
					_agendasCrt.save(persona=interr.embarazo.embarazada, mensaje=msg, fecha_con=cn[1])
				_commit()
			return (True, agendas_ids)
		except Exception, e:
			#raise e
			print e
			return (False, list())
	@classmethod
	def del_interrupt(self, id_def):
		try:
			with _db_session:
				interr = _Defuncion.get(id_def=id_def)
				interr.delete()
				_commit()
			return True
		except Exception, e:
			#raise e
			print e
			return False
	@classmethod
	def risk_status(cls, id_emb, riesgo):
		try:
			with _db_session:
				emb = cls.get_byId(id_emb); emb.set(riesgo=riesgo)
				_commit()
				return True
		except Exception, e:
			raise e
			return False
	@classmethod
	def del_risk(cls, id_emb):
		try:
			with _db_session:
				emb = cls.get_byId(id_emb); emb.set(riesgo=None)
				_commit()
				return True
		except Exception, e:
			raise e
			return False