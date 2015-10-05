#-*- coding: utf-8 -*-
from copy import deepcopy as _dcopy
from cStringIO import StringIO as _StringIO
from reportlab import rl_config as _rl_config
from reportlab.lib.units import cm as _cm
from reportlab.lib.pagesizes import (LETTER as _LETTER, landscape as _landscape, portrait as _portrait)
#from reportlab.lib.styles import (getSampleStyleSheet as _getSampleStyleSheet,)
from reportlab.lib.enums import (TA_LEFT as _TA_LEFT, TA_CENTER as _TA_CENTER, TA_RIGHT as _TA_RIGHT, TA_JUSTIFY as _TA_JUSTIFY)
from reportlab.lib import (colors as _colors,)
from reportlab.platypus import (SimpleDocTemplate as _SimpleDocTemplate, Spacer as _Spacer, PageBreak as _PageBreak)
from reportlab.platypus.tables import (LongTable as _Table, TableStyle as _TableStyle)
from reportlab.lib.styles import ParagraphStyle as _ParagraphStyle
from reportlab.platypus import Paragraph as _Paragraph
from . import getLocals as _getLocals
from . import cdict

_rl_config.defaultImageCaching = 1
#_style = _getSampleStyleSheet()
# portrait vars
_ppagesize = _portrait(_LETTER)
_ppw, _pph = _ppagesize
_p_vars = cdict(
	imgxy = dict(x=.5*_cm, y=4*_cm, anchor="c"),
	#hline = dict(x1=2.5*_cm, y1=_pph-(1.94*_cm), x2=_ppw-(1.5*_cm), y2=_pph-(1.94*_cm)),
	vline = dict(x1=2*_cm, y1=1.5*_cm, x2=2*_cm, y2=_pph-(1.94*_cm)),
	ctitle = dict(x=(_ppw/2.0)+(.5*_cm), y=_pph-(1.94*_cm)),
	date_time = dict(x=_ppw/2.0, y=1.5*_cm),
	page_count = dict(x=_ppw-(1.5*_cm), y=1.5*_cm),
	brand_name = dict(x=_pph-(7.94*_cm), y=-1.15*_cm),
)
# end portrait
# landscape vars
_lpagesize = _landscape(_LETTER)
_lpw, _lph = _lpagesize
_l_vars = cdict(
	imgxy = dict(x=5*_cm, y=2*_cm, width=18*_cm, height=18*_cm, anchor="c"),
	#hline = dict(x1=2.5*_cm, y1=_lph-(1.94*_cm), x2=_lpw-(1.5*_cm), y2=_lph-(1.94*_cm)),
	vline = dict(x1=2*_cm, y1=1.5*_cm, x2=2*_cm, y2=_lph-(1.94*_cm)),
	ctitle = dict(x=(_lpw/2.0)+(.5*_cm), y=_lph-(1.94*_cm)),
	date_time = dict(x=_lpw/2.0, y=1.5*_cm),
	page_count = dict(x=_lpw-(1.5*_cm), y=1.5*_cm),
	brand_name = dict(x=_lph-(7.94*_cm), y=-1.15*_cm),
)
# end landscape
_choice_page = lambda flag: _p_vars if flag else _l_vars
_tbstyle = _TableStyle([
	('GRID', (0,0), (-1,-1), .01*_cm, _colors.Color(.8,.8,.8)),
	('ALIGN', (0,0), (-1,-1), 'CENTER'),
	('VALIGN', (0,0), (-1,-1), 'TOP'),
	('LEFTPADDING', (0,0), (-1,-1), 3),
	('RIGHTPADDING', (0,0), (-1,-1), 3),
	('FONTSIZE', (0,1), (-1,-1), 8),
	('BOTTOMPADDING', (0,0), (-1,0), 7),
	('BACKGROUND', (0,0), (-1,0), _colors.Color(0,.352,.612,.902)),
	('TEXTCOLOR', (0,0), (-1,0), _colors.Color(1,1,1)),
	('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
	('FONTSIZE', (0,0), (-1,0), 10),
	('VALIGN', (0,0), (-1,0), 'MIDDLE'),
])

_tbstyle2cols = _TableStyle([
	('GRID', (0,0), (-1,-1), .01*_cm, _colors.Color(.8,.8,.8)),
	('ALIGN', (0,0), (-1,-1), 'CENTER'),
	('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
	('LEFTPADDING', (0,0), (-1,-1), 3),
	('RIGHTPADDING', (0,0), (-1,-1), 3),
	('FONTSIZE', (0,0), (-1,-1), 8),
	('BACKGROUND', (0,0), (0,-1), _colors.Color(.902,.902,.902, .196))
]);

def _setattribs(obj, args=[]):
	for name, value in args:
		setattr(obj, name, value)

def _base_pagemaker(canvas, doc, **kwargs):
	kwargs = cdict(kwargs)
	psize = _choice_page(kwargs.portrait)
	canvas.drawImage(image=kwargs.img_path, **psize.imgxy)
	#horizontal line
	canvas.setStrokeColorRGB(.8,.8,.8)
	canvas.setLineWidth(.01*_cm)
	#canvas.line(**psize.hline)#x1 y1 x2 y2
	#vertical line
	canvas.setStrokeColorRGB(0,.352,.612)
	canvas.setLineWidth(.6*_cm)
	canvas.line(**psize.vline)#x1 y1 x2 y2
	canvas.setFont("Helvetica-Bold", 14)
	canvas.drawCentredString(text=kwargs.title, **psize.ctitle)
	canvas.setFont("Courier", 8)
	canvas.drawString(2.5*_cm, 1.5*_cm, kwargs.user or "--")
	canvas.drawCentredString(text=u"{}, {}".format(kwargs.odate or "", kwargs.otime or ""), **psize.date_time)
	canvas.drawRightString(text=u"Página {}".format(doc.page), **psize.page_count)
	canvas.translate(_cm, _cm)
	canvas.rotate(90)
	canvas.setFillColorRGB(1,1,1)
	canvas.setFont("Helvetica-Bold", 12)
	canvas.drawString(text=u"ENLACES", x=psize.brand_name['x']+(2.7*_cm), y=psize.brand_name['y']-(.005*_cm))
	#print psize.brand_name

class ReportMaker(object):
	def __init__(self, title=u"Reporte", author=u"Enlaces", subject=u"Reporte", keywords=u"Python", creator=u"Reportlab", img_path=None, user=None, odate=None, otime=None, portrait=True):
		self.config = _getLocals(locals())
		self.config.update(dict(lang='ES', leftMargin=2.5*_cm, rightMargin=1.5*_cm, topMargin=2*_cm, bottomMargin=1.8*_cm, pagesize = _portrait(_LETTER) if portrait else _landscape(_LETTER), pageCompression=1))
		self.elements = list()
	def __FirtPage(self, canvas, doc):
		canvas.saveState()
		_base_pagemaker(canvas, doc, **self.config)
		canvas.restoreState()
	def __LaterPages(self, canvas, doc):
		canvas.saveState()
		_base_pagemaker(canvas, doc, **self.config)
		canvas.restoreState()
	def heading_content(self, heading_text, align="left", fontSize=12, sep=0):
		style = _ParagraphStyle("body")
		style.alignment = _TA_LEFT if align=="left" else _TA_CENTER if align=="center" else _TA_RIGHT if align=="right" else _TA_JUSTIFY
		_setattribs(style, [('fontName','Helvetica-Bold'),('fontSize',fontSize),('textColor','black'),('splitLongWords',1)])
		self.elements += [_Paragraph(heading_text, style), _Spacer(0, sep*_cm)]
	def body_content(self, list_content, default_style="body", align="justify", before_pg=False, after_pg=False):
		style = _ParagraphStyle(default_style)
		style.alignment = _TA_LEFT if align=="left" else _TA_CENTER if align=="center" else _TA_RIGHT if align=="right" else _TA_JUSTIFY
		self.elements += [_PageBreak()] if before_pg else list()
		self.elements += [_Paragraph(dt, style) for dt in list_content]
		self.elements += [_PageBreak()] if after_pg else list()
	def parse_datatable(self, matrix_content, fix_content = True, footer=False, towCols=False, before_pg=False, after_pg=False, cellsW=dict()):
		if not towCols:
			tb = _Table((self.__parse_datatable(matrix_content, footer=footer) if fix_content else matrix_content), repeatRows=1, **(dict(colWidths=1.5*_cm) if cellsW else dict()))
		else:
			tb = _Table(self.__parse_datatable2cols(matrix_content))
		if cellsW.keys():
			for idx, val in cellsW.iteritems():
				tb._argW[idx] = float(val)*_cm
		tb.setStyle(_tbstyle if not towCols else _tbstyle2cols)
		self.elements += [_PageBreak()] if before_pg else list()
		self.elements += [tb, _Spacer(0, .5*_cm)]
		self.elements += [_PageBreak()] if after_pg else list()
	def __parse_datatable(self, matrix_content, footer=False):
		theader = _ParagraphStyle("body")
		_setattribs(theader, [('alignment',_TA_CENTER),('fontName','Helvetica-Bold'),('fontSize',10),('textColor','white'),('wordWrap','RTL'),('splitLongWords',1)])
		tfooter = _dcopy(theader)
		_setattribs(tfooter, [('alignment',_TA_RIGHT),('wordWrap','RTL'),('textColor','black')])
		tbody = _ParagraphStyle("body")
		_setattribs(tbody, [('alignment',_TA_JUSTIFY),('fontName','Helvetica'),('fontSize',8),('wordWrap','RTL'),('splitLongWords',1)])
		parse_head = lambda text, ft_flag=False: _Paragraph(u"{}".format(text), theader) if not ft_flag else _Paragraph(u"{}".format(text), tfooter)
		parse_cell = lambda ctx, idx, jdx=-1: parse_head(ctx) if idx==0 else parse_head(ctx, True) if (idx==len(matrix_content)-1 and footer==True) else _Paragraph(ctx, tbody)
		return [[parse_cell(u"{}".format(cell), i, j) for j,cell in enumerate(row)] for i,row in enumerate(matrix_content)]
	def __parse_datatable2cols(self, matrix_content, firstRow=True):
		headingRow = _ParagraphStyle("body")
		_setattribs(headingRow, [('alignment',_TA_RIGHT),('fontName','Helvetica-Bold'),('textColor','black')])
		tbody = _ParagraphStyle("body")
		_setattribs(tbody, [('alignment', _TA_CENTER),('fontName','Helvetica'),('textColor','black')])
		parse_headingRow = lambda text, jdx=-1: _Paragraph(u'{}'.format(text), headingRow) if (firstRow and jdx==0) else _Paragraph(u'{}'.format(text), tbody)
		return [[parse_headingRow(cell, j) for j,cell in enumerate(row)] for row in matrix_content]
	@property
	def reset(self):
		self.elements = list()
	@property
	def del_lastItem(self):
		if len(self.elements):
			del self.elements[-1]
	@property
	def build_pdf(self):
		buf = _StringIO()
		sdoc = _SimpleDocTemplate(filename=buf, **self.config)
		if isinstance(self.elements[-1], _Spacer):
			del self.elements[-1]
		sdoc.build(self.elements, onFirstPage=self.__FirtPage, onLaterPages=self.__LaterPages)
		return buf.getvalue()