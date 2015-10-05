#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys, logging, signal, time
reload(sys)
sys.setdefaultencoding('utf-8')

from os import environ, path
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import (define, parse_command_line, options)

from app import App_Server

define('debug', default=False, type=bool, help='Run in debug mode')
define('port', default=8080, type=int, help='Server port')
define('localdb', default=True, type=bool, help='By default, the DB in local mode')
define('slave', default=True, type=bool, help='Slave Server to send SMS\'s')
#define('allowed_hosts', default='localhost:8080', multiple=True, help='Allowed hosts for cross domain connections')

workingdir = path.dirname(path.realpath(__file__))

def shutdown(server):
	ioloop = IOLoop.current()
	logging.info('Stopping server.')
	server.stop()
	def finalize():
		ioloop.stop()
		logging.info('Stopped.')
	ioloop.add_timeout(time.time() + .2, finalize)

if __name__ == '__main__':
	parse_command_line()
	server = HTTPServer(App_Server(workingdir))
	signal.signal(signal.SIGINT, lambda sig, frame: shutdown(server))
	logging.info('Starting server on localhost:{}'.format(options.port))
	if not options.debug:
		server.bind(environ.get('PORT', options.port))
		server.start(0)
	else:
		server.listen(environ.get('PORT', options.port))
	IOLoop.current().start()