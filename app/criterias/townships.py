#-*- coding: utf-8 -*-
from pony.orm import (db_session as _db_session, commit as _commit, flush as _flush, select as _select)
from ..entities import (Municipio as _Municipio, Comunidad as _Comunidad)
# from .communities import CommunitiesCriteria as communitiesCrt
from . import (communitiesCrt as _communitiesCrt,)

class TownshipsCriteria:
	@classmethod
	def exists(cls, nombre, dpto):
		return _Municipio.select(lambda mp: mp.nombre==nombre.upper() and mp.dpto==dpto.upper()).exists()
	@classmethod
	def get_byId(cls, id_mup):
		return _Municipio.get(id_mup=id_mup)
	@classmethod
	def get_All(cls):
		return _select(tn for tn in _Comunidad)
	@classmethod
	def save(cls, township, communities=[]):
		try:
			with _db_session:
				if not cls.exists(township.nombre, township.dpto):
					mp = _Municipio(**township); _flush()
					for cm in communities:
						cm.municipio = mp.id_mup
						_communitiesCrt.save(community=cm)
					_commit()
					return True
				return False
		except Exception, e:
			raise e
			return False
	@classmethod
	def update(cls, id_mup, nombre, dpto):
		try:
			with _db_session:
				mup = _Municipio.get(id_mup=id_mup)
				if mup.nombre==nombre.upper() and mup.dpto==dpto.upper():
					mup.set(activo=True); _commit()
					return True
				else:
					if not cls.exists(nombre, dpto):
						mup.set(nombre=nombre, dpto=dpto, activo=True); _commit()
						return True
					return False
			return True
		except Exception, e:
			raise e
			return False
	@classmethod
	def delete(cls, id_mup):
		try:
			with _db_session:
				mup = _Municipio.get(id_mup=id_mup)
				mup.set(activo=False)
				_commit()
			return False
		except Exception, e:
			#raise e
			return True