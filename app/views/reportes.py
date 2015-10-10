#-*- coding: utf-8 -*-
from pony.orm import db_session
from json import dumps
from os import (path, sep)
from urllib import urlencode
from ..tools import (route, BaseHandler, allowedRole, to_ddmmyy, to_yymmdd, cdict, ReportMaker)
from ..criterias import (DatasReport, townshipsCrt, hospitalsCrt, agendasCrt, pregnantsCrt)

@route('/reportes/catalogo')
class CatalogoMensajes(BaseHandler):
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		self.set_header('Content-type', 'application/pdf')
		params = cdict(
			img_path = path.join(path.dirname(self.settings['static_path']),'statics{}watermark.png'.format(sep)),
			title = u'Catálogo de Mensajes', user = self.current_user.persona if self.current_user else None,
			odate = to_ddmmyy(self.utc.now().date()), otime = self.utc.now().time().isoformat()[:8], portrait=False
		)
		pm = ReportMaker(**params)
		pm.parse_datatable(DatasReport.get_Catalogo(), cellsW={0:1.5,1:4,2:2.5,3:9,4:6})
		filename = urlencode(dict(filename=u'Catálogo_{}_{}.pdf'.format(params.odate.replace('/',''), params.otime.replace(':',''))))
		self.set_header('Content-Disposition', 'inline; {}'.format(filename))
		self.finish(pm.build_pdf)

@route('/reportes/mujeres')
class MujeresPDF(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		params = dict(
			townships = [cdict(id_mup=tn.id_mup, nombre=tn.nombre, centros=dumps([dict(id_cen=hp.id_cen, nombre=hp.nombre) for hp in hospitalsCrt.get_byTownship(tn.id_mup)])) for tn in townshipsCrt.get_All()],
			minDate = (pregnantsCrt.minDate() or self.utc.now().date()), maxDate = self.utc.now().date(), to_ddmmyy = to_ddmmyy
		)
		self.render('reportes/mujeres.html', **params)
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict
		params = cdict(
			img_path = path.join(path.dirname(self.settings['static_path']),'statics{}watermark.png'.format(sep)), portrait=False,
			title = u'Lista de Mujeres', user = self.current_user.persona, odate = to_ddmmyy(self.utc.now().date()), otime = self.utc.now().time().isoformat()[:8],
		)
		pm = ReportMaker(**params)
		pm.heading_content(u'(desde {} hasta {})'.format(form.f_ini, form.f_fin), align='center', fontSize=8, sep=.1)
		form.f_ini, form.f_fin = to_yymmdd(form.f_ini), to_yymmdd(form.f_fin)
		DatasReport.get_Womens(pm, start_date=form.f_ini, end_date=form.f_fin, id_cen=form.id_cen)
		self.finish(dumps(pm.build_pdf.encode('base64').replace('\n','')))

@route('/reportes/agendas')
class AgendasPDF(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		params = dict(minDate = (agendasCrt.minDate() or self.utc.now().date()), maxDate = self.utc.now().date(), to_ddmmyy = to_ddmmyy)
		self.render('reportes/agendas.html', **params)
	@db_session
	@allowedRole(u'Administrador')
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict
		params = cdict(
			img_path = path.join(path.dirname(self.settings['static_path']),'statics{}watermark.png'.format(sep)), portrait=False,
			title = u'Agendas', user = self.current_user.persona, odate = to_ddmmyy(self.utc.now().date()), otime = self.utc.now().time().isoformat()[:8],
		)
		pm = ReportMaker(**params)
		pm.heading_content(u'(desde {} hasta {})'.format(form.f_ini, form.f_fin), align='center', fontSize=8, sep=.1)
		form.f_ini, form.f_fin = to_yymmdd(form.f_ini), to_yymmdd(form.f_fin)
		DatasReport.get_RadioOperador(pm, start_date=form.f_ini, end_date=form.f_fin, notifyByRadio=False)
		self.finish(dumps(pm.build_pdf.encode('base64').replace('\n','')))

@route('/reportes/radio')
class RadioOperador(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		params = dict(minDate = (agendasCrt.minDate() or self.utc.now().date()), maxDate = self.utc.now().date(), to_ddmmyy = to_ddmmyy)
		self.render('reportes/radio.html', **params)
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict
		params = cdict(
			img_path = path.join(path.dirname(self.settings['static_path']),'statics{}watermark.png'.format(sep)), portrait=False,
			title = u'Notificaciones de Radio', user = self.current_user.persona, odate = to_ddmmyy(self.utc.now().date()), otime = self.utc.now().time().isoformat()[:8],
		)
		pm = ReportMaker(**params)
		pm.heading_content(u'(desde {} hasta {})'.format(form.f_ini, form.f_fin), align='center', fontSize=8, sep=.1)
		form.f_ini, form.f_fin = to_yymmdd(form.f_ini), to_yymmdd(form.f_fin)
		DatasReport.get_RadioOperador(pm, start_date=form.f_ini, end_date=form.f_fin)
		self.finish(dumps(pm.build_pdf.encode('base64').replace('\n','')))

@route('/reportes/global')
class Reportes(BaseHandler):
	@db_session
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'])
	def get(self):
		# tmp = hospitalsCrt.minDate()
		params = dict(
			# minDate = tmp if tmp else self.utc.now().date(),
			minDate = (hospitalsCrt.minDate() or self.utc.now().date()),
			maxDate = self.utc.now().date(), to_ddmmyy=to_ddmmyy
		)
		self.render('reportes/global.html', **params)
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		form, now = self.form2Dict, self.utc.now()
		params = cdict(
			img_path = path.join(path.dirname(self.settings['static_path']),'statics{}watermark.png'.format(sep)), portrait=False,
			title = u'Reporte por {}'.format('Municipios' if int(form.tipo)==1 else 'Establecimientos de Salud'),
			user = self.current_user.persona, odate = to_ddmmyy(now.date()), otime = now.time().isoformat()[:8],
		)
		pm = ReportMaker(**params)
		pm.heading_content(u'(desde {} hasta {})'.format(form.f_ini, form.f_fin), align='center', fontSize=8, sep=.1)
		form.f_ini, form.f_fin = to_yymmdd(form.f_ini), to_yymmdd(form.f_fin)
		DatasReport.global_Report(pm, start_date=form.f_ini, end_date=form.f_fin, default=(True if int(form.tipo)==1 else False))
		filename = 'Reporte_{}_{}.pdf'.format(params.odate.replace('/',''), params.otime.replace(':',''))
		self.set_header('Content-Disposition', 'inline; filename={}'.format(filename))
		fileencoded = pm.build_pdf.encode('base64').replace('\n','')
		self.finish(dumps(fileencoded))

@route('/reportes/historial')
class HistorialEmbarazada(BaseHandler):
	@allowedRole([u'Administrador',u'Operador de Registro',u'Operador de Radio'], True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		form, now = self.form2Dict, self.utc.now()
		params = cdict(
			img_path = path.join(path.dirname(self.settings['static_path']),'statics{}watermark.png'.format(sep)), portrait=True,
			title = u'Historial', user = self.current_user.persona, odate = to_ddmmyy(now.date()), otime = now.time().isoformat()[:8],
		)
		self.set_header('Content-Disposition', 'inline; filename=Historial_{}_{}.pdf'.format(params.odate.replace('/',''), params.otime.replace(':','')))
		pm = ReportMaker(**params)
		DatasReport.pregnant_logs(pm, form.id_per)
		fileencoded = pm.build_pdf.encode('base64').replace('\n','')
		self.finish(dumps(fileencoded))