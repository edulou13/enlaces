#-*- coding: utf-8 -*-
from . import (cdict as _cdict, utc as _utc,)
# from tornado import locale as _locale
from tornado.web import (RequestHandler as _RequestHandler, asynchronous as _asynchronous,)
from tornado.gen import (coroutine as _coroutine,)
from mako.lookup import (TemplateLookup as _TemplateLookup,)
from json import (loads as _loads,)
from datetime import (date as _date, datetime as _datetime)

def getLocals(obj):
	#return {k:v for k,v in obj.iteritems() if not(k.startswith('_') or k.startswith('self'))}
	#print type(obj), dir(obj)
	return _cdict([(k,v) for k,v in obj.iteritems() if not(k.startswith('_') or k.startswith('self') or k=='cls')])

def _form2Dict(obj):
	#return {k:obj.get_argument(k) for k in obj.request.arguments.iterkeys() if(k != '_xsrf')}
	return _cdict([(k, obj.get_argument(k)) for k in obj.request.arguments.iterkeys() if not(k.startswith('_'))])

def _dict2Obj(o_name, **params):
	return type(o_name, (object,), params)

def _obj2Dict(obj):
	check_values = lambda v: v.isoformat() if isinstance(v,_date) else '{} {}'.format(v._date().isoformat(),v.time().isoformat()[:8]) if isinstance(v,_datetime) else v
	#return {k:check_values(v) for k,v in obj.to_dict().iteritems()}
	return _cdict([(k,check_values(v)) for k,v in obj.to_dict().iteritems()])

def _cookie_user2Obj(obj, cookie_name):
	tmp = obj.get_secure_cookie(cookie_name)
	try:
		tmp = _loads(tmp)
	except TypeError:
		tmp = eval(tmp) if tmp else None
	return _dict2Obj("User", **tmp) if tmp else None

class BaseHandler(_RequestHandler):
	def initialize(self):
		# _locale.set_default_locale('es_ES')
		# print _locale.get_supported_locales()
		debug = self.application.settings['debug']
		self.lookup = _TemplateLookup(directories=[self.get_template_path()], cache_enabled=not debug, input_encoding='utf-8', output_encoding='utf-8')
	def render_string(self, template_path, **kwargs):
		template, namespace = self.lookup.get_template(template_path), self.get_template_namespace()
		namespace.update(kwargs); namespace.update(dict(format_exceptions=True))
		return template.render(**namespace)
	def render(self, template_path, **kwargs):
		self.finish(self.render_string(template_path, **kwargs))
	def get_current_user(self):
		return _cookie_user2Obj(self, "user")
	@property
	def utc(self):
		return _utc
	@property
	def form2Dict(self):
		return _form2Dict(self)
	def obj2Dict(self):
		return _obj2Dict(self)

def fullAsync(func):
	@_asynchronous
	@_coroutine
	def decorated(self, *args, **kwargs):
		return func(self, *args, **kwargs)
	return decorated

def checkRole(role, roles):
	if isinstance(roles, list):
		for r in roles:
			if r==role:
				return True
		else:
			return False
	else:
		return True if (role==roles) else False

def allowedRole(roles=None, stream=False):
	# print 'roles:{}'.format(roles)
	# print 'stream:{}'.format(stream)
	def decorator(func):
		@fullAsync
		def decorated(self, *args, **kwargs):
			# print 'class:{}'.format(self.__class__.__name__)
			if not self.current_user or (self.current_user and not checkRole(role=self.current_user.rol, roles=roles)):
				if not stream:
					self.redirect(self.reverse_url('logout'))
				return self
			return func(self, *args, **kwargs)
		return decorated
	return decorator