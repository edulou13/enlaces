#-*- coding: utf-8 -*-
from pony.orm import (db_session as _db_session, commit as _commit)
from ..entities import (Tipo as _Tipo,)

class TypesCriteria:
	@classmethod
	def check(self, nombre):
		tp = _Tipo.get(nombre=nombre.upper())
		return True if tp else False, tp.id_tip if tp else None
	@classmethod
	def save(self, nombre, descrip):
		try:
			with _db_session:
				if self.check(nombre)[0]==True:
					return False
				_Tipo(nombre=nombre, descrip=descrip); _commit()
			return True
		except Exception, e:
			return False
	@classmethod
	def update(self, id_tip, nombre, descrip):
		try:
			with _db_session:
				flag = self.check(nombre)
				if flag[0]==True and flag[1]!=int(id_tip):
					return False
				tp = _Tipo.get(id_tip=id_tip)
				tp.set(nombre=nombre, descrip=descrip, activo=True)
				_commit()
			return True
		except Exception, e:
			return False
	@classmethod
	def delete(self, id_tip):
		try:
			with _db_session:
				tp = _Tipo.get(id_tip=id_tip)
				tp.set(activo=False)
				_commit()
			return False
		except Exception, e:
			return True