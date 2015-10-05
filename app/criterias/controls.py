#-*- coding: utf-8 -*-
from pony.orm import (select as _select, count as _count, db_session as _db_session, commit as _commit)
from ..entities import (Control as _Control,)
from ..tools import (utc as _utc,)
from . import (networksCrt as _networksCrt, townshipsCrt as _townshipsCrt, hospitalsCrt as _hospitalsCrt)

class ControlsCriteria:
	@classmethod
	def total_checked(cls, id_red=None, id_mup=None, id_cen=None):
		if id_red:
			count = 0
			for mup in _networksCrt.get_byId(id_red).municipios.select():
				for com in mup.comunidades.select():
					for cn in _Control.select(lambda cn: cn.asistido):
						if cn.embarazo and cn.embarazo.embarazada.comunidad.id_com==com.id_com:
							count += 1
							continue
						if cn.recien_nacido and cn.recien_nacido.embarazo.embarazada.comunidad.id_com==com.id_com:
							count += 1
							continue
			return count
		elif id_mup:
			count = 0
			for com in _townshipsCrt.get_byId(id_mup).comunidades.select():
				for cn in _Control.select(lambda cn: cn.asistido):
					if cn.embarazo and cn.embarazo.embarazada.comunidad.id_com==com.id_com:
						count += 1
						continue
					if cn.recien_nacido and cn.recien_nacido.embarazo.embarazada.comunidad.id_com==com.id_com:
						count += 1
						continue
			return count
		elif id_cen:
			count = 0
			for com in _hospitalsCrt.get_byId(id_cen).comunidades.select():
				for cn in _Control.select(lambda cn: cn.asistido):
					if cn.embarazo and cn.embarazo.embarazada.comunidad.id_com==com.id_com:
						count += 1
						continue
					if cn.recien_nacido and cn.recien_nacido.embarazo.embarazada.comunidad.id_com==com.id_com:
						count += 1
						continue
			return count
		else:
			return _count(cn for cn in _Control if cn.asistido)
	@classmethod
	def getbyPregnancy(cls, id_emb):
		return _select(ct for ct in _Control if ct.embarazo.id_emb==id_emb).order_by(lambda ct: (ct.nro_con, ct.fecha_con))
	@classmethod
	def getbyChild(cls, id_rcn):
		return _select(ct for ct in _Control if ct.recien_nacido.id_rcn==id_rcn).order_by(lambda ct: (ct.nro_con, ct.fecha_con))
	@classmethod
	def delete_controls(cls, obj):
		check_date = lambda dt: True if dt>=_utc.now().date() else False
		with _db_session:
			for cnt in obj.controles:
				if not cnt.asistido and check_date(cnt.fecha_con):
					cnt.delete()
			_commit()