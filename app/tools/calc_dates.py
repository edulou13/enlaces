#-*- coding: utf-8 -*-
from . import utc as _utc
from datetime import (date as _date, timedelta as _timedelta)

def to_date(strDate):
	tmpDate = lambda dt: _date(int(dt[0]), int(dt[1]), int(dt[2]))
	return tmpDate(strDate.split('-'))

class BaseControl(object):
	def __init__(self, startDate, Days=True):
		self.workindays = True
		self.__tmpCtrls = [self.__to_workingDays(startDate + _timedelta(days=(i if Days else i*7))) for i in self.limits]
	def __to_workingDays(self, odate):
		return ((odate + _timedelta(days=2)) if (odate.weekday()==5) else (odate + _timedelta(days=1)) if (odate.weekday()==6) else odate) if self.workindays else odate
	def controls_dates(self):
		fixedcontrols = [(cn, dt) for cn, dt in enumerate(self.__tmpCtrls, 1) if (_utc.now().date() <= dt)]
		#assert(len(fixedcontrols))
		return fixedcontrols

class PreNatal(BaseControl):
	def __init__(self, y,m,d):
		self.limits, self.startDate = [5,16,27,36], _date(y,m,d)
		#assert(self.check_range())
		BaseControl.__init__(self, startDate=self.startDate, Days=False)
	def check_range(self):
		pp = self.startDate + _timedelta(days=280)
		days_left = (pp - _utc.now().date()).days
		return -4 <= days_left <= 280

class PostNatal(BaseControl):
	def __init__(self, y,m,d):
		self.limits = [3,7,20,28]
		BaseControl.__init__(self, startDate=_date(y,m,d))

class PrePromotional(BaseControl):
	def __init__(self, y,m,d):
		self.limits, self.workindays = [9,15,20,25,30,35], False
		BaseControl.__init__(self, startDate=_date(y,m,d), Days=False)

class PostPromotional(BaseControl):
	def __init__(self, y,m,d):
		self.limits, self.workindays = [3,7,20,28], False
		BaseControl.__init__(self, startDate=_date(y,m,d))

class Interruption(BaseControl):
	def __init__(self, y,m,d):
		self.limits, self.workindays = [1,7], False
		BaseControl.__init__(self, startDate=_date(y,m,d))

if __name__ == '__main__':
	days = [u'Lunes',u'Martes',u'Miercoles',u'Jueves',u'Viernes',u'Sábado',u'Domingo']
	y,m,d = input('>>> ')
	a = PreNatal(y,m,d)
	for ctrl in a.controls_dates()[::-1]:
		print u'control: {:2}, semana: {:2}, fecha: {}, día: {}'.format(ctrl[0],ctrl[1],ctrl[2].isoformat(),days[ctrl[2].weekday()])