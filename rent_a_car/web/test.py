# -*- coding: UTF-8 -*-

import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
arabic_text = u'تلفون'
new_word = ''
for i in arabic_text[::-1]:
	new_word = new_word+i

arabic_text = arabic_reshaper.reshape(arabic_text)
new_word = arabic_reshaper.reshape(new_word) # join characters
# arabic_text = get_display(arabic_text) # change orientation by using bidi

pdf_file=open('disclaimer.pdf','w')
pdf_doc = SimpleDocTemplate(pdf_file, pagesize=A4)
pdfmetrics.registerFont(TTFont('Arabic-normal', 'KacstOne.ttf'))
style = ParagraphStyle(name='Normal', fontName='Arabic-normal', fontSize=12, leading=12. * 1.2)
style.alignment=TA_RIGHT
pdf_doc.build([Paragraph(arabic_text, style)])
pdf_doc.build([Paragraph(arabic_text[::-1], style)])

pdf_file.close()
