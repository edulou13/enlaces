#-*- coding: utf-8 -*-
from pony.orm import (db_session as _db_session, commit as _commit)
from ..entities import (Etnia as _Etnia,)

class EthnicsCriteria:
	@classmethod
	def check(self, nombre):
		et = _Etnia.get(nombre=nombre.upper())
		return True if et else False, et.id_etn if et else None
	@classmethod
	def save(self, nombre):
		try:
			with _db_session:
				if self.check(nombre)[0]==True:
					return False
				_Etnia(nombre=nombre); _commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def update(self, id_etn, nombre):
		try:
			with _db_session:
				flag = self.check(nombre)
				if flag[0]==True and flag[1]!=int(id_etn):
					return False
				et = _Etnia.get(id_etn=id_etn)
				et.set(activo=True, nombre=nombre)
				_commit()
			return True
		except Exception, e:
			#raise e
			return False