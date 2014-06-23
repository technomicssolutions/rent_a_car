# -*- coding: utf-8 -*- 
import simplejson
import ast
from datetime import datetime
import datetime as dt
import pytz

from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.db.models import Max
from django.utils import timezone
from django.db.models import Q
from django.conf import settings

from reportlab.lib.units import cm
from reportlab.lib.units import inch
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, Image, Table, TableStyle, Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from reportlab.lib.colors import magenta, red, green, black


from web.models import *

utc=pytz.UTC

arabic_text_heading = u'الكأس الذهبي لتأجير السيارات'

tel_no = u'تلفون :'
tel_nos = '02-6266634'
mob_no = u'متحرك : '
mob_nos = '055-3020434'
po_box = u'ص.ب : '
pobox = '32900'

addrss1 = u'شارع جوازات القديم'
addrss2 = u'أبوظبي أ.ع.م'

def header(canvas):

    p = canvas
    
    p.setFont("Helvetica-Bold", 30)
    p.setFillColor(green)
    p.drawString(50, 1140, 'Golden Cup Rent A Car')
    p.setFillColor(black)

    p.setFont("Helvetica", 12)
    p.drawString(50, 1100, 'Tel : 02-6266634 , Mob : 055-4087528 , P.O.Box : 32900')
    
    p.drawString(50, 1060, 'Old Passport Road , Abu Dhabi - UAE')

    p.line(50, 1000, 1000, 1000)

    p.setFont('Arabic-normal', 20)
    p.setFillColor(green)
    p.drawString(660, 1140, arabic_text_heading[::-1])
    p.setFillColor(black)

    p.setFont('Helvetica', 13)
    p.drawString(700, 1100, '   , ')
    p.drawString(720, 1100, mob_nos)
    p.drawString(840, 1100, '   , ')
    p.drawString(860, 1100, pobox)
    p.drawString(590, 1100, tel_nos)
    p.drawString(820, 1060, '   , ')

    p.setFont('Arabic-normal', 13)
    
    p.drawString(660, 1100, tel_no[::-1])
    p.drawString(800, 1100, mob_no[::-1])
    p.drawString(900, 1100, po_box[::-1])
    p.drawString(840, 1060, addrss1[::-1])
    p.drawString(750, 1060, addrss2[::-1])

    p.setFont("Helvetica", 12)

    return p


class RentReport(View):

    def get(self, request, *args, **kwargs):
        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1050, 1200))
        y = 1160
       
        p = header(p)
        p.setFontSize(15)

        report_type = request.GET.get('report_type', '')
        if not report_type:
            return render(request, 'reports/rent_report.html', {
                'report_type' : 'date',
                })

        if report_type == 'date': 
            start = request.GET['start_date']
            end = request.GET['end_date']
           
            if not start:   
                ctx = {
                    'msg' : 'Please Select Start Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date',
                }
                return render(request, 'reports/rent_report.html', ctx)
            elif not end:
                ctx = {
                    'msg' : 'Please Select End Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date',
                }
                return render(request, 'reports/rent_report.html', ctx)                  
            else:

                y = 960
                start_date = datetime.strptime(start, '%d/%m/%Y')
                end_date = datetime.strptime(end, '%d/%m/%Y')
                p.setFontSize(17)
                p.drawString(350, y, 'Date Wise Rent Report')
                p.setFontSize(13)
                p.drawString(50, y - 55, "Date")
                p.drawString(140, y - 55, "Agreement No")
                p.drawString(240, y - 55, "Vehicle No")
                p.drawString(340, y - 55, "Plate No")
                p.drawString(440, y - 55, "Driver Name")
                p.drawString(580, y - 55, "Passport No")
                p.drawString(680, y - 55, "License No")
                p.drawString(780, y - 55, "Total Amount")
                p.drawString(880, y - 55, "Paid")
                p.drawString(950, y - 55, "Balance")

                agreements = RentAgreement.objects.filter(agreement_date__gte=start_date, agreement_date__lte=end_date).order_by('agreement_date')
                if agreements.count() > 0:
                    y = 880
                    for agreement in agreements:
                        
                        if agreement.receivecar_set.all().count() > 0:
                            total_amount = agreement.receivecar_set.all()[0].total_amount
                            paid = float(agreement.receivecar_set.all()[0].paid) + float(agreement.paid)
                        else:
                            total_amount = agreement.total_amount
                            paid = agreement.paid
                        balance = float(total_amount) - float(paid)
                        p.drawString(50, y, agreement.agreement_date.strftime('%d/%m/%Y'))
                        p.drawString(150, y, agreement.agreement_no)
                        p.drawString(240, y, agreement.vehicle.vehicle_no)
                        p.drawString(340, y, agreement.vehicle.plate_no)
                        p.drawString(440, y, agreement.driver.driver_name)
                        p.drawString(580, y, agreement.driver.driver_passport_no)
                        p.drawString(680, y, agreement.driver.driver_license_no)
                        p.drawString(780, y, str(total_amount))
                        p.drawString(880, y, str(paid))
                        p.drawString(950, y, str(balance))
                        y = y - 30
                        total_amount = 0
                        paid = 0
                        balance = 0
                        if y <= 135:
                            y = 960
                            p.showPage()
                            p = header(p)

                p.showPage()
                p.save()
                return response
        elif report_type == 'vehicle':

            start = request.GET['start_date']
            end = request.GET['end_date']
            vehicle_id = request.GET['vehicle']          
            if not start:            
                ctx = {
                    'msg' : 'Please Select Start Date ',
                    'start_date' : start,
                    'end_date' : end,
                    'vehicle' : vehicle_id,                    
                    'report_type' : 'vehicle',
                }
                return render(request, 'reports/rent_report.html', ctx)
            elif not end:
                ctx = {
                    'msg' : 'Please Select End Date',
                    'start_date' : start,
                    'end_date' : end,
                    'vehicle' : vehicle_id,
                    'report_type' : 'vehicle',
                }
                return render(request, 'reports/rent_report.html', ctx) 
            elif vehicle_id == 'select':
                ctx = {
                    'msg' : 'Please Select Vehicle',
                    'start_date' : start,
                    'end_date' : end,
                    'vehicle' : vehicle_id,
                    'report_type' : 'vehicle',
                }
                return render(request, 'reports/rent_report.html', ctx) 
            else:
                start_date = datetime.strptime(start, '%d/%m/%Y')
                end_date = datetime.strptime(end, '%d/%m/%Y')
                vehicle = Vehicle.objects.get(id=int(vehicle_id))
                p.setFontSize(17)
                y = 960
                p.drawString(350, y, 'Vehicle Wise Rent Report')
                p.setFontSize(13)
                p.drawString(50, y - 55, "Date")
                p.drawString(140, y - 55, "Agreement No")
                p.drawString(240, y - 55, "Vehicle No")
                p.drawString(340, y - 55, "Plate No")
                p.drawString(440, y - 55, "Driver Name")
                p.drawString(590, y - 55, "Passport No")
                p.drawString(720, y - 55, "Total Amount")
                p.drawString(840, y - 55, "Paid")
                p.drawString(950, y - 55, "Balance")

                agreements = RentAgreement.objects.filter(agreement_date__gte=start_date, agreement_date__lte=end_date, vehicle=vehicle).order_by('agreement_date')

                if agreements.count() > 0:
                    y = 880
                    for agreement in agreements:
                        if agreement.receivecar_set.all().count() > 0:
                            total_amount = agreement.receivecar_set.all()[0].total_amount
                            paid = float(agreement.receivecar_set.all()[0].paid) + float(agreement.paid)
                        else:
                            total_amount = agreement.total_amount
                            paid = agreement.paid
                        p.drawString(50, y, agreement.agreement_date.strftime('%d/%m/%Y'))
                        p.drawString(150, y, agreement.agreement_no)
                        p.drawString(240, y, agreement.vehicle.vehicle_no)
                        p.drawString(340, y, agreement.vehicle.plate_no)
                        p.drawString(440, y, agreement.driver.driver_name)

                        p.drawString(590, y, agreement.driver.driver_passport_no)
                        p.drawString(720, y, str(total_amount))
                        p.drawString(840, y, str(paid))
                        p.drawString(950, y, str(float(total_amount) - float(paid)))
                        y = y - 30
                        total_amount = 0
                        paid = 0
                        balance = 0
                        if y <= 135:
                            y = 960
                            p.showPage()
                            p = header(p)

                p.showPage()
                p.save()
                return response

class VehicleReport(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1050, 1200))
        y = 1160
    
        p = header(p)
        p.setFontSize(15)
        y = 960
        p.drawString(450, y, 'Vehicles Report')
        p.drawString(50,  y - 55, "Vehicle No")
        p.drawString(140,  y - 55, "Plate No")
        p.drawString(240,  y - 55, "Color")
        p.drawString(340,  y - 55, "Made")
        p.drawString(440,  y - 55, "Type")
        p.drawString(590,  y - 55, "Condition")
        p.drawString(720,  y - 55, "Meter Reading")
        p.drawString(840,  y - 55, "Insurance")
        p.drawString(950,  y - 55, "Status")

        p.setFontSize(13)
        vehicles = Vehicle.objects.all().order_by('id')
        y = 880
        if vehicles.count() > 0:
            for vehicle in vehicles:

                p.drawString(50, y, vehicle.vehicle_no)
                p.drawString(150, y, vehicle.plate_no if vehicle.plate_no and vehicle else '')
                p.drawString(240, y, vehicle.vehicle_color if vehicle.vehicle_color and vehicle else '')
                p.drawString(340, y, vehicle.vehicle_make if vehicle.vehicle_make and vehicle else '')
                p.drawString(440, y, vehicle.vehicle_type_name.vehicle_type_name if vehicle.vehicle_type_name else '')
                p.drawString(590, y, vehicle.vehicle_condition if vehicle.vehicle_condition and vehicle else '')
                p.drawString(720, y, str(vehicle.meter_reading))
                p.drawString(840, y, str(vehicle.insuranse_value))
                p.drawString(950, y, "Inside" if vehicle.is_available else "Outside")
                y = y - 30

                if y <= 135:
                    y = 960
                    p.showPage()
                    p = header(p)


        p.showPage()
        p.save()

        return response

class VehicleOutstandingReport(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1050, 1200))
        y = 1160
        p = header(p)
        p.setFontSize(15)
        y = 960
        p.drawString(450, y, 'Outstanding Vehicles Report')
        p.drawString(50,  y - 55, "Vehicle No")
        p.drawString(140,  y - 55, "Plate No")
        p.drawString(240,  y - 55, "Driver Name")
        p.drawString(440,  y - 55, "Total Amount")
        p.drawString(600,  y - 55, "Paid")
        p.drawString(700, y - 55, "Balance")
        p.drawString(800, y - 55, "Contact No")

        p.setFontSize(13)
        agreements = RentAgreement.objects.filter(vehicle__is_available=False, is_completed=False)
        y = 880
        if agreements.count() > 0:
            for agreement in agreements:

                p.drawString(50, y, agreement.vehicle.vehicle_no)
                p.drawString(150, y, agreement.vehicle.plate_no)
                p.drawString(240, y, agreement.driver.driver_name)
                p.drawString(440, y, str(agreement.total_amount))
                p.drawString(600, y, str(agreement.paid))
                p.drawString(700, y, str(float(agreement.total_amount) - float(agreement.paid)))
                p.drawString(800, y, str(agreement.driver.driver_phone))
                y = y - 30

                if y <= 135:
                    y = 960
                    p.showPage()
                    p = header(p)


        p.showPage()
        p.save()

        return response

class RevenueReport(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1050, 1200))
        y = 1160
      
        p = header(p)
        p.setFontSize(15)

        report_type = request.GET.get('report_type', '')
        if not report_type:
            return render(request, 'reports/revenue_report.html', {
                'report_type' : 'date',
                })

        if report_type == 'date': 
            start = request.GET['start_date']
            end = request.GET['end_date']
            if not start:   
                ctx = {
                    'msg' : 'Please Select Start Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date',
                }
                return render(request, 'reports/revenue_report.html', ctx)             
            else:
                start_date = datetime.strptime(start, '%d/%m/%Y')
                if not end:
                    agreements = RentAgreement.objects.filter(agreement_date=start_date).order_by('agreement_date')
                    date_range = start
                else:
                    end_date = datetime.strptime(end, '%d/%m/%Y')
                    agreements = RentAgreement.objects.filter(agreement_date__gte=start_date, agreement_date__lte=end_date).order_by('agreement_date')
                    date_range = str(start) + ' - ' + str(end)

                p.setFontSize(17)
                title_name = 'Date Wise Revenue Report - ' + str(date_range)
                y = 960
                p.drawString(350, y, title_name)
                p.setFontSize(13)
                p.drawString(50, y - 55, "Date")
                p.drawString(140, y - 55, "Agreement No")
                p.drawString(240, y - 55, "Agreement - Total Amount")
                p.drawString(420, y - 55, "Agreement - Paid")
                p.drawString(530, y - 55, "Receipt No")
                p.drawString(620, y - 55, "Receipt - Total Amount")
                p.drawString(770, y - 55, "Receipt - Paid")
                p.drawString(865, y - 55, "Driver Name")
                agreement_total = 0
                receive_total = 0
                y = 880
                if agreements.count() > 0:
                    
                    for agreement in agreements:
                        agreement_total = float(agreement_total) + float(agreement.total_amount)
                        if agreement.receivecar_set.all().count() > 0:
                            receive_total = float(receive_total) + float(agreement.receivecar_set.all()[0].total_amount)
                        p.drawString(50, y, agreement.agreement_date.strftime('%d/%m/%Y'))
                        p.drawString(150, y, agreement.agreement_no)
                        p.drawString(280, y, str(agreement.total_amount))
                        p.drawString(430, y, str(agreement.paid))
                        p.drawString(540, y, str(agreement.receivecar_set.all()[0].receipt_no) if agreement.receivecar_set.all().count() > 0 else '')
                        p.drawString(620, y, str(agreement.receivecar_set.all()[0].total_amount) if agreement.receivecar_set.all().count() > 0 else '')
                        p.drawString(780, y, str(agreement.receivecar_set.all()[0].paid) if agreement.receivecar_set.all().count() > 0 else '')
                        p.drawString(865, y, agreement.driver.driver_name)
                        y = y - 30
                        total_amount = 0
                        paid = 0
                        balance = 0
                        if y <= 135:
                            y = 960
                            p.showPage()
                            p = header(p)
                if y <= 135:
                    y = 960
                    p.showPage()
                    p = header(p)
                p.drawString(165, y, 'Agreement - Total : ')
                p.drawString(280, y, str(agreement_total))
                p.drawString(525, y, 'Receipt - Total : ')
                p.drawString(620, y, str(receive_total))

                p.showPage()
                p.save()
                return response
