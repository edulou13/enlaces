#-*- coding: utf-8 -*-
from pony.orm import (db_session as _db_session, desc as _desc)
from ..entities import (Mensaje as _Msg, Red_Salud as _Red, Persona as _Per)
from ..tools import (to_date as _to_date, to_ddmmyy as _to_ddmmyy)
from . import (hospitalsCrt as _hospitalsCrt, pregnant_status as _status, agendasCrt as _agendasCrt)

class _Index(object):
	def __init__(self):
		self.idx = 0
	@property
	def increment(self):
		self.idx += 1
		return self.idx
	@property
	def decrement(self):
		if self.idx > 0:
			self.idx -= 1
	@property
	def reset(self):
		self.idx = 0

_sumCol = lambda col, dtMatrix: reduce(lambda x,y: x+y, [i[col] for i in dtMatrix]) if len(dtMatrix) else 0

def _totalRow(dtMatrix, strTotal=u'Totales'):
	totals = [[strTotal]]
	totals[0].extend([_sumCol(i, dtMatrix[1:]) for i in range(1, len(dtMatrix[0]))])
	return totals

class _Womens:
	def __init__(self, start_date, end_date):
		_Womens.start_date, _Womens.end_date = _to_date(start_date), _to_date(end_date)
	@classmethod
	def pregnants_by_community(cls, id_com, id_cen=None):
		if not id_cen:
			return _Per.select(lambda pr: pr.sexo=='f' and pr.comunidad.id_com==id_com and pr.creado.date()>=cls.start_date and pr.creado.date()<=cls.end_date)
		else:
			return _Per.select(lambda pr: pr.sexo=='f' and pr.comunidad.id_com==id_com and pr.centro_salud.id_cen==id_cen and pr.creado.date()>=cls.start_date and pr.creado.date()<=cls.end_date)
	@classmethod
	def womens(cls, id_com, id_cen=None):
		return cls.pregnants_by_community(id_com=id_com, id_cen=id_cen).count()
	@classmethod
	def in_pregnancy(cls, id_com, id_cen=None):
		count, qfilter = 0, lambda embarazos: embarazos.select(lambda emb: (emb.creado.date()>=cls.start_date and emb.creado.date()<=cls.end_date) and emb.activo and not emb.interrupcion).order_by(lambda emb: (_desc(emb.creado),)).first()
		for pr in cls.pregnants_by_community(id_com=id_com, id_cen=id_cen):
			if qfilter(pr.embarazos):
				count += 1
		return count
	@classmethod
	def risk_pregnancies(cls, id_com, id_cen=None):
		count, qfilter = 0, lambda embarazos: embarazos.select(lambda emb: (emb.creado.date()>=cls.start_date and emb.creado.date()<=cls.end_date) and emb.activo).order_by(lambda emb: (_desc(emb.creado.date()),)).first()
		for pr in cls.pregnants_by_community(id_com=id_com, id_cen=id_cen):
			prg = qfilter(pr.embarazos)
			if prg and prg.riesgo:
				count += 1
				continue
		return count
	@classmethod
	def pre_natals(cls, id_com, id_cen=None):
		count, qfilter = 0, lambda controles: controles.select(lambda crt: (crt.creado.date()>=cls.start_date and crt.creado.date()<=cls.end_date) and crt.asistido).count()
		for pr in cls.pregnants_by_community(id_com=id_com, id_cen=id_cen):
			for emb in pr.embarazos:
				count += qfilter(emb.controles)
		return count
	@classmethod
	def mothers_death(cls, id_com, id_cen=None):
		count = 0
		for pr in cls.pregnants_by_community(id_com=id_com, id_cen=id_cen):
			if pr.defuncion and pr.defuncion.f_conf and (pr.defuncion.creado.date()>=cls.start_date and pr.defuncion.creado.date()<=cls.end_date):
				count += 1
		return count
	@classmethod
	def childrens(cls, id_com, id_cen=None):
		count = 0
		for pr in cls.pregnants_by_community(id_com=id_com, id_cen=id_cen):
			for emb in pr.embarazos:
				if emb.parto_inst:
					count += emb.recien_nacidos.select(lambda ch: ch.creado.date()>=cls.start_date and ch.creado.date()<=cls.end_date).count()
		return count
	@classmethod
	def post_natals(cls, id_com, id_cen=None):
		count, qfilter = 0, lambda controles: controles.select(lambda crt: (crt.creado.date()>=cls.start_date and crt.creado.date()<=cls.end_date) and crt.asistido).count()
		for pr in cls.pregnants_by_community(id_com=id_com, id_cen=id_cen):
			for emb in pr.embarazos:
				for ch in emb.recien_nacidos:
					count += qfilter(ch.controles)
		return count
	@classmethod
	def childrens_death(cls, id_com, id_cen=None):
		count = 0
		for pr in cls.pregnants_by_community(id_com=id_com, id_cen=id_cen):
			for emb in pr.embarazos:
				for ch in emb.recien_nacidos:
					if ch.defuncion and ch.defuncion.f_conf and (ch.creado.date()>=cls.start_date and ch.creado.date()<=cls.end_date):
						count += 1
		return count

class _Pregnant:
	def __init__(self, id_per):
		_Pregnant.pregnant = _Per.get(id_per=id_per)
	@classmethod
	def pregnant_status(cls):
		#status = lambda:u'Habilitada' if cls.pregnant.activo and not(cls.pregnant.defuncion and not cls.pregnant.defuncion.f_conf) else u'Inhabilitada' if not cls.pregnant.activo and not(cls.pregnant.defuncion and not cls.pregnant.defuncion.f_conf) else u'Advertencia de defunción' if (cls.pregnant.defuncion and not cls.pregnant.defuncion.f_conf) else 'Fallecida'
		#return status().upper()
		return _status(cls.pregnant)[1].upper()
	@classmethod
	def total_childrens(cls):
		count = 0
		for emb in cls.pregnant.embarazos:
			count += emb.recien_nacidos.count()
		return count
	@classmethod
	def all_childrens(cls):
		for emb in cls.pregnant.embarazos.select().order_by(lambda emb: (emb.creado,)):
			for ch in emb.recien_nacidos.select().order_by(lambda ch: (ch.nombres, ch.apellidos)):
				yield ch

class DatasReport:
	@classmethod
	def get_Catalogo(cls):
		idx = _Index()
		type_str = lambda tp: 'Pre-Natal' if tp==1 else 'Post-Natal' if tp==2 else 'Pre-Promocional' if tp==3 else 'Post-Promocional' if tp==4 else u'Interrupción' if tp==5 else 'Extraordinario'
		parse_data = lambda msg: [idx.increment, type_str(msg.tipo).upper(), msg.nro_control, msg.tenor, msg.usuario.persona.__str__()]
		table = [['#', 'Tipo', 'Control', 'Tenor', 'Usuario']]
		with _db_session:
			table.extend([parse_data(msg) for msg in _Msg.select(lambda msg: msg.tipo>=1 and msg.tipo<=5).order_by(lambda msg: (msg.tipo, msg.nro_control))])
		return table
	def __delete(self, repr_maker):
		check = lambda idx=-1: repr_maker.elements[-1].__class__.__name__ == ('Spacer' or 'Paragraph')
		if check() and check(-2):
			repr_maker.del_lastItem
			repr_maker.del_lastItem
	@classmethod
	def get_RadioOperador(cls, repr_maker, start_date, end_date):
		start_date, end_date = _to_date(start_date), _to_date(end_date)
		type_str = lambda tp: 'Pre-Natal' if tp==1 else 'Post-Natal' if tp==2 else 'Pre-Promocional' if tp==3 else 'Post-Promocional' if tp==4 else u'Interrupción' if tp==5 else 'Extraordinario'
		titles = [u'Mujer',u'Tipo de Mensaje',u'Control',u'Fecha de Control',u'Fecha de Notificación', u'Usuario']
		section, subsection, sub_subsection = _Index(), _Index(), _Index()
		for red in _Red.select(lambda red: red.activo).order_by(lambda red: (red.nombre,)):
			red_status = False
			repr_maker.heading_content(u'{}.- Red de Salud: {}'.format(section.increment, red.__str__()), align='justify', sep=.3)
			for mup in red.municipios.select(lambda mup: mup.activo).order_by(lambda mup: (mup.nombre,)):
				mup_status = False
				repr_maker.heading_content(u'{}.{}.- Municipio: {}, {}'.format(section.idx, subsection.increment, mup.__str__(), mup.dpto), align='justify', sep=.3)
				for com in mup.comunidades.select(lambda com: com.activo).order_by(lambda com: (com.nombre,)):
					repr_maker.heading_content(u'{}.{}.{}.- Comunidad: {}'.format(section.idx, subsection.idx, sub_subsection.increment, com.__str__()), align='justify', sep=.3)
					table = [titles]
					for ag in _agendasCrt.get_forReport(id_com=com.id_com, start_date=start_date, end_date=end_date):
						table.extend([[ag.persona.__str__(), type_str(ag.mensaje.tipo), ag.mensaje.nro_control, _to_ddmmyy(ag.fecha_con), (_to_ddmmyy(ag.modificado.date()) if ag.rad_estado else ''), (ag.usuario.persona.__str__() if ag.usuario else '')]])
					if len(table) > 1:
						repr_maker.parse_datatable(table, cellsW={0:6,1:4,2:1.7,3:2.5,4:2.5,5:6})
						mup_status = True if not mup_status else mup_status
						red_status = True if not red_status else red_status
					else:
						cls().__delete(repr_maker)
						sub_subsection.decrement
				if not mup_status:
					subsection.decrement
					cls().__delete(repr_maker)
				sub_subsection.reset
			if not red_status:
				section.decrement
				cls().__delete(repr_maker)
			subsection.reset
		# print len(repr_maker.elements)
		# for i,row in enumerate(repr_maker.elements):
		# 	print i, type(row), row.__class__.__name__
		# 	if i==50:
		# 		break
	@classmethod
	@_db_session
	def global_Report(cls, repr_maker, start_date, end_date, default=True):
		titles = [u'Comunidad',u'Mujeres Registradas',u'Mujeres en Gestación',u'Embarazos de Riesgo',u'Controles Pre-Natales',u'Defunciones Maternas',u'Recién Nacidos',u'Controles Post-Natales',u'Defunciones R. Nacidos']
		wms, section, subsection = _Womens(start_date=start_date, end_date=end_date), _Index(), _Index()
		row_data = lambda com, id_cen=None: [[com.__str__(), wms.womens(com.id_com, id_cen=id_cen), wms.in_pregnancy(com.id_com, id_cen=id_cen),wms.risk_pregnancies(com.id_com, id_cen=id_cen), wms.pre_natals(com.id_com, id_cen=id_cen), wms.mothers_death(com.id_com, id_cen=id_cen), wms.childrens(com.id_com, id_cen=id_cen), wms.post_natals(com.id_com, id_cen=id_cen), wms.childrens_death(com.id_com, id_cen=id_cen)]]
		for rd in _Red.select(lambda rd: rd.activo==True).order_by(lambda rd: (rd.nombre,)):
			repr_maker.heading_content(u'{}.- Red de Salud: {}'.format(section.increment, rd.__str__()), align='justify', sep=.3)
			if default:
				for mup in rd.municipios.select(lambda mup: mup.activo).order_by(lambda mup: (mup.nombre,)):
					repr_maker.heading_content(u'{}.{}.- Municipio: {}, {}'.format(section.idx, subsection.increment, mup.__str__(), mup.dpto), align='justify', sep=.3)
					table = [titles]
					for com in mup.comunidades.select(lambda com: com.activo).order_by(lambda com: (com.nombre,)):
						table.extend(row_data(com=com))
					table.extend(_totalRow(table, strTotal=u'Sub-Totales'))
					repr_maker.parse_datatable(table, footer=True, cellsW={0:4.5,1:2.4,2:2.4,3:2.4,4:2.4,5:2.4,6:2.4,7:2.4,8:2.4})
				subsection.reset
			else:
				for hp in _hospitalsCrt.get_byNetwork(id_red=rd.id_red):
					repr_maker.heading_content(u'{}.{}.- Establecimiento de Salud: {}, Municipio: {}, {}'.format(section.idx, subsection.increment, hp.__str__(), hp.ubicado.municipio.__str__(), hp.ubicado.municipio.dpto), align='justify', sep=.3)
					table = [titles]
					for com in hp.comunidades.select(lambda com: com.activo).order_by(lambda com: (com.nombre,)):
						table.extend(row_data(com=com, id_cen=hp.id_cen))
					table.extend(_totalRow(table, strTotal=u'Sub-Totales'))
					repr_maker.parse_datatable(table, footer=True, cellsW={0:4.5,1:2.4,2:2.4,3:2.4,4:2.4,5:2.4,6:2.4,7:2.4,8:2.4})
				subsection.reset
	@classmethod
	@_db_session
	def pregnant_logs(cls, repr_maker, id_per):
		pr = _Pregnant(id_per=id_per)
		repr_maker.heading_content('', sep=.1)
		repr_maker.heading_content(pr.pregnant.__str__(), align='center', fontSize=14, sep=.5)
		table = [
			[u'Fecha de Nacimiento:', _to_ddmmyy(pr.pregnant.f_nac)], [u'Edad:', u'{} años'.format(pr.pregnant.current_age())],
			[u'Nro. de Embarazos:', pr.pregnant.embarazos.count()], [u'Nro. de Hijos:', pr.total_childrens()],
			[u'Celular:', pr.pregnant.telf or ''], [u'Estado:', pr.pregnant_status()],
			[u'Municipio:', u'{}, {}'.format(pr.pregnant.comunidad.municipio.__str__(), pr.pregnant.comunidad.municipio.dpto)],
			[u'Comunidad:',pr.pregnant.comunidad.__str__() or ''], [u'Establecimiento de Salud:', pr.pregnant.centro_salud.__str__()],
			[u'Contacto:', pr.pregnant.contacto.__str__() or ''], [u'Relación o Parentesco:', pr.pregnant.relacion or ''],
			[u'Celular de{} Contacto:'.format(' la' if pr.pregnant.contacto.sexo=='f' else 'l'), pr.pregnant.contacto.telf],
		]
		repr_maker.parse_datatable(table, towCols=True, cellsW={0:5,1:6})
		row_idx = _Index()
		repr_maker.heading_content(u'Embarazos:', fontSize=12, sep=.3)
		table = [[u'#', u'Parto Probable', u'Fecha de Parto', u'Nro. de Hijos', u'Riesgo', u'Fecha de Interrupción']]
		for emb in pr.pregnant.embarazos.select().order_by(lambda emb: (emb.creado,)):
			table.extend([[
				row_idx.increment, _to_ddmmyy(emb.parto_prob), _to_ddmmyy(emb.parto_inst) if emb.parto_inst else '', emb.recien_nacidos.count(),
				emb.riesgo or '', _to_ddmmyy(emb.interrupcion.f_conf) if (emb.interrupcion and emb.interrupcion.f_conf) else '',
			]])
		if len(table) > 1:
			row_idx.reset
			repr_maker.parse_datatable(table, cellsW={0:1,1:2,2:2,3:2,4:7,5:3})
		else:
			cls().__delete(repr_maker)
		repr_maker.heading_content(u'Hijos/Hijas:', fontSize=12, sep=.3)
		table = [[u'#', u'Nombres y Apellidos', u'Fecha de Nacimiento', u'Sexo', u'Peso']]
		for ch in pr.all_childrens():
			table.extend([[
				row_idx.increment, ch.__str__(), _to_ddmmyy(ch.embarazo.parto_inst),
				u'Femenino' if ch.sexo=='f' else u'Masculino', u'{} kgrs.'.format(ch.peso)
			]])
		if len(table) > 1:
			repr_maker.parse_datatable(table, cellsW={0:1,1:7.7,2:2.3,3:3,4:3})
		else:
			cls().__delete(repr_maker)