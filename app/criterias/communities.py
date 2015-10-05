#-*- coding: utf-8 -*-
from pony.orm import (db_session as _db_session, commit as _commit, flush as _flush, select as _select)
from ..entities import (Municipio as _Municipio, Comunidad as _Comunidad)
#from .hospitals import HospitalsCriteria as hospitalsCrt
from . import (hospitalsCrt as _hospitalsCrt,)

class CommunitiesCriteria:
	@classmethod
	def exists(cls, id_mup, nombre):
		return _Municipio.get(id_mup=id_mup).comunidades.select(lambda cm: cm.nombre==nombre.upper()).exists()
	@classmethod
	def get_All(self):
		return _select(cm for cm in _Comunidad).order_by(lambda cm: (cm.municipio, cm.nombre))
	@classmethod
	def save(self, community, hospitals=[]):
		try:
			with _db_session:
				if not self.exists(id_mup=community.municipio, nombre=community.nombre):
					com = _Comunidad(**community); _flush()
					for hp in hospitals:
						hp.ubicado = com.id_com
						_hospitalsCrt.save(hospital=hp, communities=[com.id_com])
					_commit()
					return True
				return False
		except Exception, e:
			raise e
			return False
	@classmethod
	def update(self, id_com, nombre, telf):
		try:
			with _db_session:
				com = _Comunidad.get(id_com=id_com)
				com.set(nombre=nombre, telf=telf, activo=True)
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def delete(self, id_com):
		try:
			with _db_session:
				com = _Comunidad.get(id_com=id_com)
				com.set(activo=False)
				_commit()
			return False
		except Exception, e:
			#raise e
			return True