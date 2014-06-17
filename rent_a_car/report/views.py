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


from web.models import *

utc=pytz.UTC

def header(canvas):

    p = canvas
    style = [
        ('FONTSIZE', (0,0), (-1, -1), 20),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
    ]

    new_style = [
        ('FONTSIZE', (0,0), (-1, -1), 30),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
    ]

    para_style = ParagraphStyle('fancy')
    para_style.fontSize = 32
    para_style.fontName = 'Helvetica-Bold'
    para = Paragraph('Golden Cup Rent A Car', para_style)

    data =[[ para , '']]
    
    table = Table(data, colWidths=[500, 100], rowHeights=50, style=style)
    table.wrapOn(p, 200, 400)
    table.drawOn(p, 300, 1160) 

    path = settings.PROJECT_ROOT.replace("\\", "/")+"/header/trophy.jpg"
    p.drawImage(path, 70, 1045, width=30*cm, height=3*cm, preserveAspectRatio=True)
    p.setFont("Helvetica", 12)
    p.drawString(350, 1020, 'Tel : 02-6266634 , Mob : 055-4087528 , P.O.Box : 32900')
    p.drawString(400, 1006, 'Old Passport Road , Abu Dhabi - UAE')
    p.line(50, 960, 1000, 960)

    return p


class RentReport(View):

    def get(self, request, *args, **kwargs):
        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1050, 1200))
        y = 1160
        style = [
            ('FONTSIZE', (0,0), (-1, -1), 20),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
        ]

        new_style = [
            ('FONTSIZE', (0,0), (-1, -1), 30),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
        ]

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
                start_date = datetime.strptime(start, '%d/%m/%Y')
                end_date = datetime.strptime(end, '%d/%m/%Y')
                p.setFontSize(17)
                p.drawString(350, 930, 'Date Wise Rent Report')
                p.setFontSize(13)
                p.drawString(50, 875, "Date")
                p.drawString(140, 875, "Agreement No")
                p.drawString(240, 875, "Vehicle No")
                p.drawString(340, 875, "Plate No")
                p.drawString(440, 875, "Driver Name")
                p.drawString(580, 875, "Passport No")
                p.drawString(680,875, "License No")
                p.drawString(780, 875, "Total Amount")
                p.drawString(880, 875, "Paid")
                p.drawString(950, 875, "Balance")

                agreements = RentAgreement.objects.filter(agreement_date__gte=start_date, agreement_date__lte=end_date).order_by('agreement_date')
                if agreements.count() > 0:
                    y = 850
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
                            y = 850
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
                p.drawString(350, 930, 'Vehicle Wise Rent Report')
                p.setFontSize(13)
                p.drawString(50, 875, "Date")
                p.drawString(140, 875, "Agreement No")
                p.drawString(240, 875, "Vehicle No")
                p.drawString(340, 875, "Plate No")
                p.drawString(440, 875, "Driver Name")
                p.drawString(590,875, "Passport No")
                p.drawString(720, 875, "Total Amount")
                p.drawString(840, 875, "Paid")
                p.drawString(950, 875, "Balance")

                agreements = RentAgreement.objects.filter(agreement_date__gte=start_date, agreement_date__lte=end_date, vehicle=vehicle).order_by('agreement_date')

                if agreements.count() > 0:
                    y = 850
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
                            y = 850
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
        style = [
            ('FONTSIZE', (0,0), (-1, -1), 20),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
        ]

        new_style = [
            ('FONTSIZE', (0,0), (-1, -1), 30),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
        ]

        p = header(p)
        p.setFontSize(15)
        p.drawString(450, 930, 'Vehicles Report')
        p.drawString(50, 875, "Vehicle No")
        p.drawString(140, 875, "Plate No")
        p.drawString(240, 875, "Color")
        p.drawString(340, 875, "Made")
        p.drawString(440, 875, "Type")
        p.drawString(590,875, "Condition")
        p.drawString(720, 875, "Meter Reading")
        p.drawString(840, 875, "Insurance")
        p.drawString(950, 875, "Status")

        p.setFontSize(13)
        vehicles = Vehicle.objects.all().order_by('id')
        y = 850
        if vehicles.count() > 0:
            for vehicle in vehicles:

                p.drawString(50, y, vehicle.vehicle_no)
                p.drawString(150, y, vehicle.plate_no)
                p.drawString(240, y, vehicle.vehicle_color)
                p.drawString(340, y, vehicle.vehicle_make)
                p.drawString(440, y, vehicle.vehicle_type_name.vehicle_type_name if vehicle.vehicle_type_name else '')
                p.drawString(590, y, vehicle.vehicle_condition)
                p.drawString(720, y, str(vehicle.meter_reading))
                p.drawString(840, y, str(vehicle.insuranse_value))
                p.drawString(950, y, "Inside" if vehicle.is_available else "Outside")
                y = y - 30

                if y <= 135:
                    y = 850
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
        style = [
            ('FONTSIZE', (0,0), (-1, -1), 20),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
        ]

        new_style = [
            ('FONTSIZE', (0,0), (-1, -1), 30),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
        ]

        p = header(p)
        p.setFontSize(15)
        p.drawString(450, 930, 'Outstanding Vehicles Report')
        p.drawString(50, 875, "Vehicle No")
        p.drawString(140, 875, "Plate No")
        p.drawString(240, 875, "Client Name")
        p.drawString(440, 875, "Total Amount")
        p.drawString(600, 875, "Paid")
        p.drawString(700,875, "Balance")

        p.setFontSize(13)
        agreements = RentAgreement.objects.filter(vehicle__is_available=False, is_completed=False)
        y = 850
        if agreements.count() > 0:
            for agreement in agreements:

                p.drawString(50, y, agreement.vehicle.vehicle_no)
                p.drawString(150, y, agreement.vehicle.plate_no)
                p.drawString(240, y, agreement.client.name)
                p.drawString(440, y, str(agreement.total_amount))
                p.drawString(600, y, str(agreement.paid))
                p.drawString(700, y, str(float(agreement.total_amount) - float(agreement.paid)))
                y = y - 30

                if y <= 135:
                    y = 850
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
        style = [
            ('FONTSIZE', (0,0), (-1, -1), 20),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
        ]

        new_style = [
            ('FONTSIZE', (0,0), (-1, -1), 30),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
        ]

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
                p.drawString(350, 930, title_name)
                p.setFontSize(13)
                p.drawString(50, 875, "Date")
                p.drawString(140, 875, "Agreement No")
                p.drawString(240, 875, "Agreement - Total Amount")
                p.drawString(420, 875, "Agreement - Paid")
                p.drawString(530, 875, "Receipt No")
                p.drawString(620, 875, "Receipt - Total Amount")
                p.drawString(770, 875, "Receipt - Paid")
                p.drawString(865, 875, "Driver Name")
                agreement_total = 0
                receive_total = 0
                y = 850
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
                            y = 850
                            p.showPage()
                            p = header(p)
                if y <= 135:
                    y = 850
                    p.showPage()
                    p = header(p)
                p.drawString(165, y, 'Agreement - Total : ')
                p.drawString(280, y, str(agreement_total))
                p.drawString(525, y, 'Receipt - Total : ')
                p.drawString(620, y, str(receive_total))

                p.showPage()
                p.save()
                return response
