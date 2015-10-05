#-*- coding: utf-8 -*-
from pony.orm import (db_session, select, desc)
from datetime import timedelta
from json import dumps
from ..tools import (route, BaseHandler, allowedRole, to_ddmmyy)
from ..entities import (Mensaje,)
from ..criterias import (messagesCrt, agendasCrt, personsCrt)
from .. import sendsms2sedes

@route('/mensajes/gestion')
class MensajesGestion(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		#print self.application.slave_server
		mensajes = select(msg for msg in Mensaje if msg.tipo!=6).order_by(lambda msg: (msg.tipo, msg.nro_control, desc(msg.creado)))
		self.render('mensajes/gestion.html', mensajes=mensajes)

@route('/mensajes/before_save')
class BeforeSave(BaseHandler):
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(messagesCrt.before_save(**self.form2Dict)))

@route('/mensajes/adicionar_msj')
class AdicionarMsj(BaseHandler):
	@allowedRole(u'Administrador')
	def get(self):
		slave = self.application.slave_server
		self.render('mensajes/adicionar_msj.html', slave=slave)
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict
		form.audio = self.rename_audio(form.tipo, form.nro_control)
		params = dict(
			status = messagesCrt.save(form=form, id_user=self.current_user.id),
			audio = form.audio
		)
		self.finish(dumps(params))
	def rename_audio(self, numb_status, numb_control, ext='mp3'):
		status = ['prenatal','postnatal','prom_prenatal','prom_postnatal','interrup']
		return '{}_{:02}.{}'.format(status[int(numb_status)-1], int(numb_control), ext)

@route('/mensajes/modificar_msj')
class ModificarMsj(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		msg = Mensaje.get(**self.form2Dict)
		self.render('mensajes/modificar.html',msg=msg)
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type','application/json')
		flag = messagesCrt.update(id_user=self.current_user.id, **self.form2Dict)
		self.finish(dumps(flag))

@route('/mensajes/eliminar_msj')
class EliminarMsj(BaseHandler):
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type','application/json')
		flag = messagesCrt.delete(id_user=self.current_user.id, **self.form2Dict)
		self.finish(dumps(flag))

@route('/mensajes/sendsms')
class SendSMS(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		persons = personsCrt.get_All()
		self.render('mensajes/sendsms.html', personas=persons)
	@db_session
	@allowedRole(u'Administrador', True)
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict; form.tipo = 6
		if form.has_key('id_per'):
			del form.id_per
		#print form
		self.msg = messagesCrt.save(form=form, id_user=self.current_user.id, default=False)
		if self.msg:
			self.personas = [id_per for id_per in self.get_arguments('id_per') if len(id_per)]
			sendsms2sedes(self)
		self.finish(dumps(True))
	def persons2Json(self):
		contact = lambda pr: dict(contacto=pr.contacto.__str__(), ctelf=pr.contacto.telf) if not pr.telf else dict()
		person = lambda pr: dict(id_per=pr.id_per, nombre=pr.__str__(), telf=(pr.telf or None), **contact(pr))
		return dumps([person(personsCrt.get_byId(id_per)) for id_per in self.personas])

@route('/mensajes/agendas')
class Agendas(BaseHandler):
	@db_session
	@allowedRole(u'Administrador')
	def get(self):
		today = self.utc.now().date()
		params = dict(
			today = to_ddmmyy(today), yesterday = to_ddmmyy((today - timedelta(days=1))), tomorrow = to_ddmmyy((today + timedelta(days=1))),
			agendas = agendasCrt.get_all().filter(lambda ag: ag.mensaje.tipo>=1 and ag.mensaje.tipo<=5),
			to_ddmmyy = to_ddmmyy
		)
		#print params
		self.render('mensajes/agendas.html', **params)

"""
@route('/mensajes/renderpdf', name='renderpdf')
class PreviewPdf(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		self.set_header('Content-type', 'application/pdf')
		dt, hr, messages = to_ddmmyy(self.utc.now().date()), self.utc.now().time().isoformat()[:8], messagesCrt.get_Catalogo()
		params = dict(fecha=dt, hora=hr, messages=messages)
		pdf = create_pdf(self.render_string('mensajes/report_msg.html', **params))
		self.set_header('Content-Disposition', 'inline; filename="Catálogo_f{}h{}.pdf"'.format(dt, hr))
		#self.set_header('Content-Disposition', 'attachment; filename=Catálogo_f{}h{}.pdf'.format(dt, hr))
		self.finish(pdf)
		#self.finish('<embed type="application/pdf" src="data:application/pdf;base64,{}" style="width:100%;height:100%;"/>'.format(pdf.encode('base64').replace('\n','')))

@route('/mensajes/report', name='report')
class ReportEmbed(BaseHandler):
	@asynchronous
	@coroutine
	def get(self):
		#self.set_header('Content-type', 'application/pdf')
		client = AsyncHTTPClient()
		#response = yield Task(client.fetch, HTTPRequest('http://localhost/mensajes/renderpdf', method='GET'))
		response = yield client.fetch('http://localhost/mensajes/renderpdf')
		pdfencoded = response.body.encode('base64').replace('\n','')
		self.finish('<embed type="application/pdf" src="data:application/pdf;base64,{}" style="width:100%;height:100%;"/>'.format(pdfencoded))
"""