#-*- coding: utf-8 -*-
from pony.orm import (db_session as _db_session, commit as _commit)
from ..entities import (Prestacion as _Prestacion,)

class CapabilitiesCriteria:
	@classmethod
	def check(self, nombre):
		cp = _Prestacion.get(nombre=nombre.upper())
		return True if cp else False, cp.id_pst if cp else None
	@classmethod
	def get_byId(cls, id_pst):
		return _Prestacion.get(id_pst=id_pst)
	@classmethod
	def save(self, nombre, descrip):
		try:
			with _db_session:
				if self.check(nombre)[0]==True:
					return False
				_Prestacion(nombre=nombre, descrip=descrip); _commit()
			return True
		except Exception, e:
			return False
	@classmethod
	def update(self, id_pst, nombre, descrip):
		try:
			with _db_session:
				flag = self.check(nombre)
				if flag[0]==True and flag[1]!=int(id_pst):
					return False
				pr = _Prestacion.get(id_pst=id_pst)
				pr.set(nombre=nombre, descrip=descrip, activo=True)
				_commit()
			return True
		except Exception, e:
			return False
	@classmethod
	def delete(self, id_pst):
		try:
			with _db_session:
				pr = _Prestacion.get(id_pst=id_pst)
				pr.set(activo=False)
				if not pr.centros_salud.is_empty():
					pr.centros_salud.clear()
				_commit()
			return False
		except Exception, e:
			return True