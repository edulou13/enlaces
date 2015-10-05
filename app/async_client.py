#-*- coding: utf-8 -*-
from json import loads as _loads
from urllib import urlencode as _urlencode
from tornado.gen import coroutine as _coroutine, Task as _Task, Return as _Return
from tornado.httpclient import AsyncHTTPClient as _AsyncHTTPClient
from criterias import (agendasCrt as _agendasCrt, messagesCrt as _messagesCrt)

_AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')

@_coroutine
def asyncClient(link, data):
	response = yield _Task(_AsyncHTTPClient().fetch, **dict(request=link, method='POST', body=data, expect_100_continue=True, request_timeout=120.0))
	raise _Return(_loads(response.body)) if response.body else _Return(None)

@_coroutine
def sendsms2sedes(cls):
	link, data = '{host}:{port}/sendsms'.format(**cls.application.slave_server), _urlencode(dict(msg=cls.msg.tenor, personas=cls.persons2Json()))
	print link
	response = yield asyncClient(link=link, data=data)
	if response:
		for id_per in cls.personas:
			_agendasCrt.save(persona=id_per, mensaje=cls.msg.id_msj)
	else:
		_messagesCrt.delete(id_msj=cls.msg.id_msj, id_user=cls.current_user.id)

@_coroutine
def deleteAgendasOnSedes(cls, agendas=list()):
	#print cls.application.slave_server
	print '{}: {}'.format(cls.__class__.__name__, agendas)
	if isinstance(agendas, list) and len(agendas):
		link, data = '{host}:{port}/delete_agendas'.format(**cls.application.slave_server), _urlencode(dict(agendas=agendas))
		response = yield asyncClient(link=link, data=data)
		if response:
			print 'Agendas has been delete on SEDES'
		else:
			print 'Lost connection with SEDES'