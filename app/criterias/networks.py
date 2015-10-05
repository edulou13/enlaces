#-*- coding: utf-8 -*-
from pony.orm import (db_session as _db_session, commit as _commit, flush as _flush, select as _select)
from ..entities import (Red_Salud as _Red_Salud,)
#from .townships import TownshipsCriteria as townshipsCrt
from . import (townshipsCrt as _townshipsCrt,)

class NetworksCtriteria:
	@classmethod
	def exists(cls, nombre):
		return _Red_Salud.select(lambda rd: rd.nombre==nombre.upper()).exists()
	@classmethod
	def get_byId(cls, id_red):
		return _Red_Salud.get(id_red=id_red)
	@classmethod
	def get_All(cls):
		return _select(nt for nt in _Red_Salud).order_by(lambda nt: (nt.nombre,))
	@classmethod
	def save(cls, form):
		try:
			with _db_session:
				if not cls.exists(nombre=form.nombre):
					red = _Red_Salud(nombre=form.nombre); _flush()
					for mp in form.municipios:
						mp.red_salud = red.id_red
						_townshipsCrt.save(township=mp)
					_commit()
					return True
				return False
		except Exception, e:
			raise e
			return False
	@classmethod
	def update(cls, id_red, nombre):
		try:
			with _db_session:
				red = _Red_Salud.get(id_red=id_red)
				if red.nombre==nombre.upper():
					red.set(activo=True); _commit()
					return True
				else:
					if not cls.exists(nombre):
						red.set(nombre=nombre, activo=True); _commit()
						return True
					return False
		except Exception, e:
			raise e
			return False