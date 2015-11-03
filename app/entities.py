#-*- coding: utf-8 -*-
from datetime import (date as _date, datetime as _datetime)
from tools import (utc as _utc,)
from pony.orm import (Database as _Database, PrimaryKey as _PrimaryKey, Required as _Required, Optional as _Optional, Set as _Set)
from json import dumps as _dumps

db = _Database()

class Red_Salud(db.Entity):
	id_red = _PrimaryKey(int, auto=True)
	nombre = _Required(unicode, unique=False)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	activo = _Optional(bool, default=True)
	municipios = _Set(lambda: Municipio, reverse='red_salud')
	operadores = _Set(lambda: Usuario, reverse='red_salud')
	def before_insert(self):
		self.nombre = self.nombre.upper()
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.nombre = self.nombre.upper()
		self.modificado = _utc.now()
	def __str__(self):
		return u'{}'.format(self.nombre)

class Municipio(db.Entity):
	id_mup = _PrimaryKey(int, auto=True)
	dpto = _Required(unicode)
	nombre = _Required(unicode)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	activo = _Optional(bool, default=True)
	red_salud = _Required(Red_Salud, reverse='municipios')
	comunidades = _Set(lambda: Comunidad, reverse='municipio')
	operadores = _Set(lambda: Usuario, reverse='municipio')
	def before_insert(self):
		self.nombre = self.nombre.upper()
		self.dpto = self.dpto.upper()
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.nombre = self.nombre.upper()
		self.dpto = self.dpto.upper()
		self.modificado = _utc.now()
	def __str__(self):
		return u'{}'.format(self.nombre)

class Comunidad(db.Entity):
	id_com = _PrimaryKey(int, auto=True)
	nombre = _Required(unicode)
	telf = _Optional(unicode, 8)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	activo = _Optional(bool, default=True)
	municipio = _Required(Municipio, reverse='comunidades')
	centros_salud = _Set(lambda: Centro_Salud, reverse='ubicado')
	atendido = _Set(lambda: Centro_Salud, reverse='comunidades')
	personas = _Set(lambda: Persona, reverse='comunidad')
	def before_insert(self):
		self.nombre = self.nombre.upper()
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.nombre = self.nombre.upper()
		self.modificado = _utc.now()
	def __str__(self):
		return u'{}'.format(self.nombre)

class Centro_Salud(db.Entity):
	id_cen = _PrimaryKey(int, auto=True)
	tipo = _Required(unicode)
	encargado = _Optional('Persona', reverse='asignado', nullable=True)
	nombre = _Required(unicode)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	activo = _Optional(bool, default=True)
	ubicado = _Required(Comunidad, reverse='centros_salud')
	comunidades = _Set(Comunidad, reverse='atendido')
	prestaciones = _Set(lambda: Prestacion, reverse='centros_salud')
	operadores = _Set(lambda: Usuario, reverse='centro_salud')
	empleados = _Set(lambda: Persona, reverse='centro_trabajo')
	embarazadas = _Set(lambda: Persona, reverse='centro_salud')
	def before_insert(self):
		self.nombre = self.nombre.upper()
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.nombre = self.nombre.upper()
		self.modificado = _utc.now()
	def __str__(self):
		return u'{}'.format(self.nombre)

class Prestacion(db.Entity):
	id_pst = _PrimaryKey(int, auto=True)
	nombre = _Required(unicode, unique=False)
	descrip = _Optional(unicode, nullable=True)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	activo = _Optional(bool, default=True)
	centros_salud = _Set(Centro_Salud, reverse='prestaciones')
	def before_insert(self):
		self.nombre = self.nombre.upper()
		self.descrip = self.descrip.upper() if self.descrip else None
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.nombre = self.nombre.upper()
		self.descrip = self.descrip.upper() if self.descrip else None
		self.modificado = _utc.now()
	def __str__(self):
		return u'{}'.format(self.nombre)

class Tipo(db.Entity):
	id_tip = _PrimaryKey(int, auto=True)
	nombre = _Required(unicode, unique=False)
	descrip = _Optional(unicode, nullable=True)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	activo = _Optional(bool, default=True)
	personas = _Set(lambda: Persona, reverse='tipos')
	def before_insert(self):
		self.nombre = self.nombre.upper()
		self.descrip = self.descrip.upper() if self.descrip else None
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.nombre = self.nombre.upper()
		self.descrip = self.descrip.upper() if self.descrip else None
		self.modificado = _utc.now()
	def __str__(self):
		return u'{}'.format(self.nombre)

class Etnia(db.Entity):
	id_etn = _PrimaryKey(int, auto=True)
	nombre = _Required(unicode, unique=False)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	activo = _Optional(bool, default=True)
	personas = _Set(lambda: Persona, reverse='etnia')
	def before_insert(self):
		self.nombre = self.nombre.upper()
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.nombre = self.nombre.upper()
		self.modificado = _utc.now()
	def __str__(self):
		return u'{}'.format(self.nombre)

class Persona(db.Entity):
	id_per = _PrimaryKey(int, auto=True)
	ci = _Optional(unicode, 11, nullable=True)
	telf = _Optional(str, 8, nullable=True)
	nombres = _Required(unicode)
	apellidos = _Required(unicode)
	sexo = _Required(str, 1, default='f')
	f_nac = _Optional(_date, nullable=True)
	idioma = _Required(unicode, default=u'Castellano')
	defuncion = _Optional(lambda: Defuncion, reverse='embarazada', nullable=True)
	cobertura = _Optional(int, default=1)
	activo = _Optional(bool, default=True)
	relacion = _Optional(unicode, nullable=True)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	tipos = _Set(Tipo, reverse='personas')
	etnia = _Optional(Etnia, reverse='personas', nullable=True)
	comunidad = _Optional(Comunidad, reverse='personas', nullable=True)
	contacto = _Optional(lambda: Persona, reverse='embarazadas')
	embarazadas = _Set(lambda: Persona, reverse='contacto')
	usuario = _Optional(lambda: Usuario, reverse='persona')
	embarazos = _Set(lambda: Embarazo, reverse='embarazada')
	asignado = _Optional(lambda: Centro_Salud, reverse='encargado', nullable=True)
	centro_trabajo = _Optional(lambda: Centro_Salud, reverse='empleados', nullable=True)
	agendas = _Set(lambda: Agenda, reverse='persona')
	centro_salud = _Optional(Centro_Salud, reverse='embarazadas')
	def before_insert(self):
		self.nombres = self.nombres.upper()
		self.apellidos = self.apellidos.upper()
		self.creado = self.modificado = _utc.now()
		if self.relacion:
			self.relacion = self.relacion.upper()
	def before_update(self):
		self.nombres = self.nombres.upper()
		self.apellidos = self.apellidos.upper()
		if self.relacion:
			self.relacion = self.relacion.upper()
		self.modificado = _utc.now()
	def current_age(self):
		return _utc.now().date().year - self.f_nac.year
	def to_dict(self):
		return dict(
				id_per = self.id_per, telf = self.telf or None, cobertura = self.cobertura, nombres = self.nombres,
				apellidos = self.apellidos, contacto = (self.contacto.id_per if self.contacto else None)
			)
	def __str__(self):
		return u'{} {}'.format(self.nombres, self.apellidos).replace('  ',' ')

class Usuario(db.Entity):
	persona = _PrimaryKey(Persona, reverse='usuario')
	rol = _Required(unicode)
	alcance = _Optional(unicode, 1, nullable=True)
	login = _Required(unicode, 24, unique=True)
	passwd = _Required(str)
	red_salud = _Optional(Red_Salud, reverse='operadores', nullable=True)
	municipio = _Optional(Municipio, reverse='operadores', nullable=True)
	centro_salud = _Optional(Centro_Salud, reverse='operadores', nullable=True)
	#embarazos = _Set(lambda: Embarazo, reverse='usuario')
	mensajes = _Set(lambda: Mensaje, reverse='usuario')
	agendas = _Set(lambda: Agenda, reverse='usuario')
	activo = _Optional(bool, default=True)
	def before_insert(self):
		self.passwd = self.passwd.encode('hex').encode('base64').replace('\n','')
	def to_json(self):
		f_alcance = lambda key: dict(alcance=self.alcance, **f_asignaciones(key)) if key>=1 else {}
		f_asignaciones = lambda key: f_red() if key==2 else f_mup() if key==3 else f_cen() if key==4 else {}
		f_red = lambda: dict(red_salud=dict(id_red=self.red_salud.id_red, nombre=self.red_salud.nombre))
		f_mup = lambda: dict(municipio=dict(id_mup=self.municipio.id_mup, nombre=self.municipio.nombre))
		f_cen = lambda: dict(centro_salud=dict(id_cen=self.centro_salud.id_cen, nombre=self.centro_salud.nombre))
		return _dumps(dict(persona=self.persona.__str__(), id=self.persona.id_per, rol=self.rol, login=self.login, **f_alcance(int(self.alcance or '0'))))
	def __str__(self):
		return u'{}'.format(self.login)

class Embarazo(db.Entity):
	id_emb = _PrimaryKey(int, auto=True)
	tipo = _Optional(int, nullable=True)
	parto_prob = _Required(_date)
	parto_inst = _Optional(_date, nullable=True)
	#usuario = _Required(Usuario, reverse='embarazos')
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	activo = _Optional(bool, default=True)
	riesgo = _Optional(unicode, nullable=True)
	interrupcion = _Optional(lambda: Defuncion, reverse='embarazo', nullable=True)
	embarazada = _Required(Persona, reverse='embarazos')
	recien_nacidos = _Set(lambda: Recien_Nacido, reverse='embarazo')
	controles = _Set(lambda: Control, reverse='embarazo')
	def before_insert(self):
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.modificado = _utc.now()

class Recien_Nacido(db.Entity):
	id_rcn = _PrimaryKey(int, auto=True)
	sexo = _Required(str, 1, default='f')
	peso = _Required(float)
	nombres = _Optional(unicode, nullable=True)
	apellidos = _Optional(unicode)
	f_nac = _Optional(_date, nullable=True)
	defuncion = _Optional(lambda: Defuncion, reverse='recien_nacido', nullable=True)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	#activo = _Optional(bool, default=True)
	embarazo = _Required(Embarazo, reverse='recien_nacidos')
	controles = _Set(lambda: Control, reverse='recien_nacido')
	def before_insert(self):
		self.nombres = self.nombres.upper()
		self.apellidos = self.apellidos.upper()
		self.f_nac = self.embarazo.parto_inst
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.nombres = self.nombres.upper()
		self.apellidos = self.apellidos.upper()
		self.modificado = _utc.now()
	def current_age(self):
		return (_utc.now().date() - self.embarazo.parto_inst).days
	def __str__(self):
		return u'{} {}'.format(self.nombres or '', self.apellidos).strip()

class Defuncion(db.Entity):
	id_def = _PrimaryKey(int, auto=True)
	embarazada = _Optional(Persona, reverse='defuncion', nullable=True)
	embarazo = _Optional(Embarazo, reverse='interrupcion', nullable=True)
	recien_nacido = _Optional(Recien_Nacido, reverse='defuncion', nullable=True)
	fecha = _Required(_date)
	f_notf = _Required(_date)
	f_conf = _Optional(_date, nullable=True)
	obs_notf = _Required(unicode)
	obs_conf = _Optional(unicode, nullable=True)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	def before_insert(self):
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.modificado = _utc.now()

class Mensaje(db.Entity):
	id_msj = _PrimaryKey(int, auto=True)
	nro_control = _Optional(int, nullable=True)
	tipo = _Required(int)
	tenor = _Required(unicode)
	audio = _Optional(unicode, nullable=True)
	activo = _Optional(bool, default=True)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	agendas = _Set(lambda: Agenda, reverse='mensaje')
	usuario = _Optional(Usuario, reverse='mensajes')
	def before_insert(self):
		self.tenor = self.tenor.upper()
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.tenor = self.tenor.upper()
		self.modificado = _utc.now()
	def to_dict(self):
		return dict(
				id_msj = self.id_msj, nro_control = self.nro_control or None,
				tipo = self.tipo, tenor = self.tenor, audio = self.audio or None
			)

class Control(db.Entity):
	id_cnt = _PrimaryKey(int, auto=True)
	tipo = _Required(unicode, default=u'Pre-Natal')
	nro_con = _Required(int)
	fecha_con = _Required(_date)
	asistido = _Required(bool, default=False)
	observacion = _Optional(unicode, nullable=True)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	embarazo = _Optional(Embarazo, reverse='controles', nullable=True)
	recien_nacido = _Optional(Recien_Nacido, reverse='controles', nullable=True)
	def before_insert(self):
		self.observacion = self.observacion.upper() if self.observacion else None
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.modificado = _utc.now()

class Agenda(db.Entity):
	id_agd = _PrimaryKey(int, auto=True)
	persona = _Required(Persona, reverse='agendas')
	mensaje = _Required(Mensaje, reverse='agendas')
	fecha_msj = _Required(_date)
	fecha_con = _Optional(_date, nullable=True)
	sms_estado = _Optional(bool, default=False, nullable=True)
	lmd_estado = _Optional(bool, default=False, nullable=True)
	rad_estado = _Optional(bool, default=False, nullable=True)
	creado = _Optional(_datetime)
	modificado = _Optional(_datetime)
	usuario = _Optional(Usuario, nullable=True, reverse='agendas')
	#_PrimaryKey(persona, mensaje)
	def before_insert(self):
		self.creado = self.modificado = _utc.now()
	def before_update(self):
		self.modificado = _utc.now()
	def to_dict(self):
		return dict(id_agd = self.id_agd, mensaje = self.mensaje.id_msj, persona = self.persona.id_per, fecha_msj = self.fecha_msj.isoformat(), fecha_con = self.fecha_con.isoformat(), sms_estado=self.sms_estado, lmd_estado=self.lmd_estado)

if __name__ == '__main__':
	def load(developdb):
		from pony.orm import (sql_debug, commit, db_session, flush)
		from tools import LoadConfig
		from os import path
		wk = path.dirname(path.dirname(path.realpath(__file__)))
		conf = LoadConfig(wk).conf()
		sql_debug(True)
		#db.bind('sqlite', 'telesalud.sqlite', create_db=True)
		loadconf = lambda: conf.developdb if developdb else conf.productiondb
		db.bind('postgres', **loadconf())
		db.generate_mapping(create_tables=True)
		with db_session:
			[Tipo(nombre=nm) for nm in [u'Embarazada',u'Contacto']]; flush()
			pr = Persona(telf='76180435',ci='5669297',nombres=u'Luis Eduardo',apellidos=u'Miranda Barja',sexo='m')
			Usuario(persona=pr, login=u'eduardo',passwd=u'Mast3R',rol=u'Administrador'); commit()
	print u' True for developdb or False for productiondb'
	load(input('>>> '))