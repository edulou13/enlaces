#-*- coding: utf-8 -*-
from ..tools import (cdict,)
from pony.orm import (db_session as _db_session, commit as _commit, flush as _flush, select as _select)
from ..entities import (Persona as _Persona, Usuario as _Usuario, Red_Salud as _Red_Salud, Municipio as _Municipio, Centro_Salud as _Centro_Salud)

def _user_form(form):
	f_asignacion = lambda key: dict(red_salud=_Red_Salud.get(id_red=form.id_red)) if key==2 else dict(municipio=_Municipio.get(id_mup=form.id_mup)) if key==3 else dict(centro_salud=_Centro_Salud.get(id_cen=form.id_cen)) if key==4 else {}
	f_alcance = lambda: dict(alcance=form.alcance, **f_asignacion(int(form.alcance)) if int(form.alcance)>1 else {}) if form.has_key('alcance') else {}
	return cdict(login=form.login,passwd=form.passwd,rol=form.rol, **f_alcance())

class UsersCriteria:
	@classmethod
	def get(self, **kwargs):
		return _Usuario.get(**kwargs)
	@classmethod
	def get_all(self):
		return (us for us in _Usuario.select().order_by(lambda us: (us.rol, us.login)))
	@classmethod
	def v_login(self, login):
		try:
			with _db_session:
				return _select(us for us in _Usuario if us.login==login).exists()
		except Exception, e:
			print e
			return False
	@classmethod
	def granted_access(self, form):
		if len(form.login) and len(form.passwd):
			form.activo, form.passwd = True, form.passwd.encode('hex').encode('base64').replace('\n','')
			return _Usuario.get(**form)
		else:
			return None
	@classmethod
	def save(self, form):
		try:
			with _db_session:
				if not form.has_key('nombres'):
					pr = _Persona.get(telf=form.telf)
					pr.set(ci=form.ci); _flush()
				else:
					f_persona = lambda: dict(telf=form.telf,ci=form.ci,nombres=form.nombres,apellidos=form.apellidos,sexo=form.sexo)
					pr = _Persona(**f_persona())
				_Usuario(persona=pr, **_user_form(form)); _commit()
			return True
		except Exception, e:
			print e
			return False
	@classmethod
	def update(self, form):
		try:
			with _db_session:
				us = _Usuario.get(persona=form.persona)
				if us:
					if form.has_key('ci'):
						us.persona.set(nombres=form.nombres, apellidos=form.apellidos, ci=form.ci, telf=form.telf); _flush()
						del form.nombres; del form.apellidos; del form.ci; del form.telf
						f_usuario = form
					else:
						us.set(alcance=None, red_salud=None, municipio=None, centro_salud=None, activo=True); _flush()
						f_usuario = _user_form(form)
					if len(f_usuario.passwd):
						f_usuario.passwd = f_usuario.passwd.encode('hex').encode('base64').replace('\n','')
					else:
						del f_usuario.passwd
					#print f_usuario
					us.set(**f_usuario)
					_commit()
				else:
					return False
			return True
		except Exception, e:
			print e
			return False
	@classmethod
	def delete(self, persona):
		try:
			with _db_session:
				us = _Usuario.get(persona=persona)
				if us:
					us.set(activo=False); _commit()
			return False
		except Exception, e:
			print e
			return True