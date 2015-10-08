#-*- coding: utf-8 -*-
from pony.orm import (db_session as _db_session, commit as _commit, select as _select)
from ..entities import (Mensaje as _Mensaje, Usuario as _Usuario)

class MessagesCriteria:
	limits = {1:[1,2,3,4], 2:[1,2,3,4], 3:[1,2,3,4,5,6], 4:[1,2,3,4], 5:[1,2]}
	@classmethod
	def before_save(cls, tipo):
		tipo = int(tipo)
		nro_control = 1
		with _db_session:
			for msg in _Mensaje.select(lambda msg: msg.tipo==tipo):
				if msg.nro_control in cls.limits[tipo]:
					nro_control += 1
					continue
		return nro_control if(nro_control in cls.limits[tipo]) else -1
	@classmethod
	def get_byNumbControl(self, nro_control, tipo=1):
		return _Mensaje.get(nro_control=nro_control, tipo=tipo, activo=True)
	@classmethod
	def get_api(self):
		for msg in _Mensaje.select(lambda msg: msg.tipo>=1 and msg.tipo<=5).order_by(lambda msg: (msg.id_msj,)):
			yield msg
	@classmethod
	def check(self, tipo, nro_control):
		with _db_session:
			return _select(msg for msg in _Mensaje if int(nro_control)==msg.nro_control and int(tipo)==msg.tipo and msg.activo==True).exists()
	@classmethod
	def save(self, form, id_user, default=True):
		flag = self.check(nro_control=form.nro_control,tipo=form.tipo) if hasattr(form,'nro_control') else False
		#print flag
		if not flag:
			with _db_session:
				user = _Usuario.get(persona=id_user)
				msg = _Mensaje(usuario=user, **form); _commit()
		return not flag if default else msg
	@classmethod
	def update(self, id_msj, tenor, id_user):
		with _db_session:
			user = _Usuario.get(persona=id_user)
			msg = _Mensaje.get(id_msj=id_msj)
			msg.set(tenor=tenor, activo=True, usuario=user); _commit()
		return True
	@classmethod
	def delete(self, id_msj, id_user):
		with _db_session:
			user = _Usuario.get(persona=id_user)
			msg = _Mensaje.get(id_msj=id_msj)
			msg.set(activo=False, usuario=user); _commit()
		return msg.activo