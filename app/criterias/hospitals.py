#-*- coding: utf-8 -*-
from pony.orm import (db_session as _db_session, commit as _commit, flush as _flush, min as _min)
from ..entities import Centro_Salud as _Hospital, Comunidad as _Community
#from .capabilities import CapabilityCriteria as _capabilitiesCrt
from . import (capabilitiesCrt as _capabilitiesCrt)

class HospitalsCriteria:
	@classmethod
	def exists(cls, nombre, ubicado):
		return _Hospital.select(lambda hp: hp.nombre==nombre.upper() and hp.ubicado.id_com==int(ubicado)).exists()
	@classmethod
	def get_byId(cls, id_cen):
		return _Hospital.get(id_cen=id_cen)
	@classmethod
	def minDate(cls):
		return _min(hp.creado.date() for hp in _Hospital)
	@classmethod
	def get_all(cls):
		return _Hospital.select().order_by(lambda hp: (hp.ubicado, hp.nombre))
	@classmethod
	def get_byNetwork(cls, id_red):
		return _Hospital.select(lambda hp: hp.activo and hp.ubicado.municipio.red_salud.id_red==id_red).order_by(lambda hp: (hp.ubicado, hp.nombre))
	@classmethod
	def get_byTownship(cls, id_mup):
		return _Hospital.select(lambda hp: hp.activo and hp.ubicado.municipio.id_mup==id_mup).order_by(lambda hp: (hp.nombre,))
	def set_hospitals_and_capabilities(self, hospital, communities=[], capabilities=[]):
		if not hospital.comunidades.is_empty():
			hospital.comunidades.clear()
			hospital.comunidades += [hospital.ubicado]
		for id_com in communities:
			hospital.comunidades += [_Community.get(id_com=id_com)]
		if not hospital.prestaciones.is_empty():
			hospital.prestaciones.clear()
		for id_pst in capabilities:
			hospital.prestaciones += [_capabilitiesCrt.get_byId(id_pst=id_pst)]
	@classmethod
	def save(cls, hospital, communities=[], capabilities=[]):
		print "Hospital", hospital, communities, capabilities
		try:
			with _db_session:
				if not cls.exists(nombre=hospital.nombre, ubicado=hospital.ubicado):
					hp = _Hospital(**hospital); _flush()
					cls().set_hospitals_and_capabilities(hp, communities, capabilities)
					_commit()
					return True
				return False
		except Exception, e:
			raise e
			return False
	@classmethod
	def update(cls, hospital, communities=[], capabilities=[]):
		try:
			with _db_session:
				hp = cls.get_byId(id_cen=hospital.id_cen)
				cls().set_hospitals_and_capabilities(hp, communities, capabilities)
				if hospital.nombre.upper()==hp.nombre:
					hp.set(nombre=hospital.nombre, tipo=hospital.tipo, activo=True); _commit()
					return True
				else:
					if not cls.exists(hospital.nombre, hp.ubicado.id_com):
						hp.set(nombre=hospital.nombre, tipo=hospital.tipo, activo=True); _commit()
						return True
					return False
		except Exception, e:
			raise e
			return False