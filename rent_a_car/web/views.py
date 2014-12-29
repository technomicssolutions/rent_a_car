# -*- coding: utf-8 -*- 
import simplejson
import ast
from datetime import datetime
import datetime as dt
import pytz
import arabic_reshaper

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


import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.styles import ParagraphStyle

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import magenta, red, green, black


from web.models import *

utc=pytz.UTC

# font_path = settings.PROJECT_ROOT.replace("\\", "/")+"/header/KacstOne.ttf"
font_path_regular = settings.PROJECT_ROOT.replace("\\", "/")+"/header/AdobeArabic-Regular.ttf"
# font_path_regular = settings.PROJECT_ROOT.replace("\\", "/")+"/header/AdobeArabic-Italic.ttf"
# font_path_regular = settings.PROJECT_ROOT.replace("\\", "/")+"/header/AdobeArabic-BoldItalic.ttf"
font_path_bold = settings.PROJECT_ROOT.replace("\\", "/")+"/header/AdobeArabic-Bold.ttf"
# font_path = settings.PROJECT_ROOT.replace("\\", "/")+"/header/AdobeArabic-Bold.ttf"
pdfmetrics.registerFont(TTFont('Arabic-normal', font_path_regular))
pdfmetrics.registerFont(TTFont('Arabic-bold', font_path_bold))


path = settings.PROJECT_ROOT.replace("\\", "/")+"/header/trophy.jpg"

arabic_text_total_amount = u'المبلغ الاجمالي'
arabic_text_address = u'عنوان'
arabic_text_dob = u'تاريخ ميلاد'
arabic_text_tel = u'تلفون'
arabic_text_time = u'الوقت'
arabic_text_date = u'التاريخ'
arabic_text_driver_name = u'اسم السائق'
arabic_text_license_no = u'رقم رخصة'
arabic_text_passport_no = u'رقم الجواز'
arabic_text_nationality = u'الجنسية'
arabic_text_sponsar_name = u'اسم الكفيل'
arabic_text_sponsar_tel = u'تلفون  الكفيل'
arabic_text_sponsar_address = u'عنوان الكفيل'
arabic_text_paid = u'مدفوع'
arabic_text_balance = u'توازن'
arabic_text_passport_issue_date = u'جواز سفر التاريخ'
arabic_text_issued_place = u'أصدرت مكان'
arabic_text_license_type = u'نوع الترخيص'
arabic_text_emirates_id = u'بطاقة هوية المقيمين'
arabic_text_vehicle_scratch = u'خدش السيارة'
arabic_text_accident = u'حادث مقبول'
arabic_text_heading = u'الكأس الذهبي لتأجير السيارات'

tel_no = u'تلفون :'
tel_nos = '02-6266634'
mob_no = u'متحرك : '
mob_nos = '055-3020434'
po_box = u'ص.ب : '
pobox = '32900'
fax_no = '02-6420741'

arabic_text_fax_no = u'الفاكس :'

addrss1 = u'شارع جوازات القديم'
addrss2 = u'أبوظبي أ.ع.م'


def draw_heading(canvas):
    p = canvas
    p.setFont('Arabic-bold', 30)
    p.setFillColor(green)
    p.drawString(600, 1160, arabic_text_heading[::-1])
    p.setFillColor(black)

    p.setFont('Helvetica', 13)
    p.drawString(700, 1120, '   , ')
    p.drawString(720, 1120, mob_nos)
    p.drawString(840, 1120, '   , ')
    p.drawString(860, 1120, pobox)
    p.drawString(590, 1120, tel_nos)
    p.drawString(830, 1095, fax_no)
    p.drawString(820, 1070, '   , ')

    p.setFont('Arabic-normal', 18)
    
    p.drawString(660, 1120, tel_no[::-1])
    p.drawString(800, 1120, mob_no[::-1])
    p.drawString(900, 1120, po_box[::-1])
    p.drawString(900, 1095, arabic_text_fax_no[::-1])
    p.drawString(840, 1070, addrss1[::-1])
    p.drawString(750, 1070, addrss2[::-1])
    return p

class Home(View):

    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, 'home.html',context)

class Login(View):

    def post(self, request, *args, **kwargs):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user and user.is_active:
            login(request, user)
        else:
            context = {
                'message' : 'Username or password is incorrect'
            }
            return render(request, 'home.html',context)
        return HttpResponseRedirect(reverse('home'))

class Logout(View):

    def get(self, request, *args, **kwargs):

        logout(request)
        return HttpResponseRedirect(reverse('home'))

class AddVehicle(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'add_vehicle.html', context)

    def post(self, request, *args, **kwargs):

        ctx_vehicle_data = []
        status = 200 
        if request.is_ajax():
            vehicle_details = ast.literal_eval(request.POST['vehicle_details'])
            try:
                try:
                    vehicle = Vehicle.objects.get(vehicle_no=vehicle_details['vehicle_no'])
                    message = 'Vehicle with this Vehicle No is already existing'
                except Exception as ex:
                    vehicle = Vehicle.objects.get(plate_no=vehicle_details['plate_no'])
                    message = 'Vehicle with this Plate No is already existing'
                res = {
                    'result': 'error',
                    'message': message,
                }
                
            except Exception as ex:
                print str(ex)
                vehicle = Vehicle.objects.create(vehicle_no=vehicle_details['vehicle_no'],plate_no=vehicle_details['plate_no'])
                
                vehicle_type, vehicle_created = VehicleType.objects.get_or_create(vehicle_type_name=vehicle_details['vehicle_type'])
                vehicle.vehicle_type_name = vehicle_type
                vehicle.vehicle_color = vehicle_details['color']
                vehicle.meter_reading = vehicle_details['meter_reading']
                vehicle.vehicle_condition = vehicle_details['condition']
                if vehicle_details['insurance_value']:
                    vehicle.insuranse_value = float(vehicle_details['insurance_value'])
                vehicle.type_of_insuranse = vehicle_details['insurance_type']
                vehicle.vehicle_make = vehicle_details['vehicle_make']
                vehicle.petrol = vehicle_details['petrol']
                vehicle.save()
                ctx_vehicle_data.append({
                    'id': vehicle.id,
                    'vehicle_no': vehicle.vehicle_no,
                    'plate_no': vehicle.plate_no,
                    'vehicle_type': vehicle.vehicle_type_name.vehicle_type_name,
                    'meter_reading': vehicle.meter_reading,
                    'vehicle_condition': vehicle.vehicle_condition,
                    'color': vehicle.vehicle_color,
                    'insuranse_value': vehicle.insuranse_value,
                    'type_of_insuranse': vehicle.type_of_insuranse,
                    'petrol': vehicle.petrol if vehicle.petrol else 0,
                })
                res = {
                    'result': 'ok',
                    'vehicle_data': ctx_vehicle_data,
                }
                status = 200

            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')



class VehicleList(View):

    def get(self, request, *args, **kwargs):

        ctx_vehicles = []
        ctx_whole_vehicles = []
        if request.is_ajax():
            whole_vehicles = Vehicle.objects.all().order_by('id')
            vehicles = Vehicle.objects.filter(is_available=True).order_by('id')
            if vehicles.count() > 0:
                for vehicle in vehicles:
                    ctx_vehicles.append({
                        'id': vehicle.id,
                        'vehicle_no': vehicle.vehicle_no,
                        'plate_no': vehicle.plate_no,
                        'vehicle_type': vehicle.vehicle_type_name.vehicle_type_name if vehicle.vehicle_type_name else '',
                        'meter_reading': vehicle.meter_reading,
                        'vehicle_condition': vehicle.vehicle_condition,
                        'color': vehicle.vehicle_color,
                        'insuranse_value': vehicle.insuranse_value,
                        'type_of_insuranse': vehicle.type_of_insuranse,
                        'petrol': vehicle.petrol if vehicle.petrol else 0,
                    })
            if whole_vehicles.count() > 0:
                for vehicle in whole_vehicles:
                    ctx_whole_vehicles.append({
                        'id': vehicle.id,
                        'vehicle_no': vehicle.vehicle_no,
                        'plate_no': vehicle.plate_no,
                        'vehicle_type': vehicle.vehicle_type_name.vehicle_type_name if vehicle.vehicle_type_name else '',
                        'meter_reading': vehicle.meter_reading,
                        'vehicle_condition': vehicle.vehicle_condition,
                        'color': vehicle.vehicle_color,
                        'insuranse_value': vehicle.insuranse_value,
                        'type_of_insuranse': vehicle.type_of_insuranse,
                        'petrol': vehicle.petrol if vehicle.petrol else 0,
                    })
            res = {
                'vehicles': ctx_vehicles,
                'whole_vehicles': ctx_whole_vehicles,
            }
            response = simplejson.dumps(res)
            status = 200
            return HttpResponse(response, status=status, mimetype='application/json')
        else:
            vehicles = Vehicle.objects.all().order_by('id')
        context = {
            'vehicles': vehicles,
        }

        return render(request, 'vehicles.html', context)

class AddVehicleType(View):

    def post(self, request, *args, **kwargs):

        if request.is_ajax():

            new_vehicle_type, created = VehicleType.objects.get_or_create(vehicle_type_name=request.POST['vehicle_type'])

            res = {
                'result': 'ok',
                'vehicle_type_name': new_vehicle_type.vehicle_type_name,
            }

            response = simplejson.dumps(res)

            status = 200

            return HttpResponse(response, status=status, mimetype='application/json')

class VehicleTypeList(View):

    def get(self, request, *args, **kwargs):

        vehicle_types = VehicleType.objects.all().order_by('id')

        ctx_vehicle_types = []

        if request.is_ajax():
            if vehicle_types.count() > 0:
                for vehicle_type in vehicle_types:
                    ctx_vehicle_types.append({
                        'vehicle_type': vehicle_type.vehicle_type_name,
                    })
            res = {
                'result': 'ok',
                'vehicle_types': ctx_vehicle_types,
            }
            status = 200
            response = simplejson.dumps(res)

            return HttpResponse(response, status=status, mimetype='application/json')

class EditVehicle(View):

    def get(self, request, *args, **kwargs):

        vehicle_id = kwargs['vehicle_id']
        ctx_vehicle = []
        vehicle = Vehicle.objects.get(id=int(vehicle_id))
        if request.is_ajax():
            ctx_vehicle.append({
                'vehicle_no': vehicle.vehicle_no,
                'plate_no': vehicle.plate_no,
                'condition': vehicle.vehicle_condition,
                'vehicle_type': vehicle.vehicle_type_name.vehicle_type_name,
                'color': vehicle.vehicle_color,
                'meter_reading': vehicle.meter_reading,
                'insurance_type': vehicle.type_of_insuranse,
                'insurance_value': vehicle.insuranse_value,
                'vehicle_make': vehicle.vehicle_make,
                'petrol': vehicle.petrol,
            })
            res = {
                'vehicle': ctx_vehicle,
            }
            status = 200
            response = simplejson.dumps(res)

            return HttpResponse(response, status=status, mimetype='application/json')
        context = {
            'vehicle_id': vehicle.id,
        }

        return render(request, 'edit_vehicle.html', context)
    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            status = 200
            vehicle_id = kwargs['vehicle_id']
            print vehicle_id
            vehicle = Vehicle.objects.get(id=int(vehicle_id))
            vehicle_details = ast.literal_eval(request.POST['vehicle_details'])
            vehicle_type = VehicleType.objects.get(vehicle_type_name=vehicle_details['vehicle_type'])
            # try:
            vehicles = Vehicle.objects.filter(vehicle_no = vehicle_details['vehicle_no']).exclude(id=vehicle_id).count()
            if vehicles:
                res = {
                    'result': 'error',
                    'message': 'Vehicle with this vehicle number exists',
                }
                response = simplejson.dumps(res)
                return HttpResponse(response, status=status, mimetype='application/json')
            else:
                vehicle.vehicle_no = vehicle_details['vehicle_no']
           
            vehicles = Vehicle.objects.filter(plate_no = vehicle_details['plate_no']).exclude(id=vehicle_id).count()
            if vehicles:
                res = {
                    'result': 'error',
                    'message': 'Vehicle with this plate number exists',
                }
                response = simplejson.dumps(res)
                return HttpResponse(response, status=status, mimetype='application/json')
            else:
                vehicle.plate_no = vehicle_details['plate_no']
            
            vehicle.vehicle_type_name = vehicle_type
            vehicle.vehicle_color = vehicle_details['color']
            vehicle.meter_reading = vehicle_details['meter_reading']
            vehicle.vehicle_condition = vehicle_details['condition']
            vehicle.insuranse_value = vehicle_details['insurance_value']
            vehicle.type_of_insuranse = vehicle_details['insurance_type']
            vehicle.vehicle_make = vehicle_details['vehicle_make']
            vehicle.petrol = vehicle_details['petrol']
            vehicle.save()
            res = {
                'result': 'ok'
            }
                
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class RentAgreementView(View):

    def get(self, request, *args, **kwargs):


        agreement_id = RentAgreement.objects.aggregate(Max('id'))['id__max']
        if not agreement_id:
            agreement_id = 1
        else:
            agreement_id = agreement_id + 1
        context = {
            'agreement_no': agreement_id,
        }

        return render(request, 'rent_agreement.html', context)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            rent_agreement_details = ast.literal_eval(request.POST['rent_agreement'])
            try:
                rent_agreement, agreement_created = RentAgreement.objects.get_or_create(agreement_no=rent_agreement_details['agreement_no'])
                vehicle = Vehicle.objects.get(id=int(rent_agreement_details['vehicle_id']))
                rent_agreement.vehicle = vehicle
                vehicle.meter_reading = request.POST['vehicle_meter_reading']
                vehicle.save()
                rent_agreement.leaving_meterreading = request.POST['vehicle_meter_reading']
                rent_agreement.leaving_petrol = vehicle.petrol
                rent_agreement.client_identity = rent_agreement_details['client_identity']
                rent_agreement.agreement_date = datetime.strptime(rent_agreement_details['date'], '%d/%m/%Y')
                start_date_time = utc.localize(datetime.strptime(rent_agreement_details['start_date_time'], '%d/%m/%Y %I:%M%p'))
                end_date_time = utc.localize(datetime.strptime(rent_agreement_details['end_date_time'], '%d/%m/%Y %I:%M%p' ))
                rent_agreement.starting_date_time = start_date_time
                rent_agreement.end_date_time = end_date_time
                print rent_agreement_details['rent_type']
                rent_agreement.rent_type = rent_agreement_details['rent_type']
                rent_agreement.vehicle_scratch = rent_agreement_details['vehicle_scratch']
                rent_agreement.accident_passable = rent_agreement_details['accident_passable']
                driver = Driver.objects.get(id=int(rent_agreement_details['driver_id']))
                rent_agreement.driver = driver
                rent_agreement.notes = rent_agreement_details['notes']
                rent_agreement.total_amount = rent_agreement_details['amount']
                rent_agreement.rent = rent_agreement_details['rent']
                rent_agreement.paid = rent_agreement_details['paid']
                rent_agreement.rental_entitled_in_km = rent_agreement_details['rental_in_km']
                rent_agreement.liable_to_pay_in_km = rent_agreement_details['liable_to_pay_in_km']
                rent_agreement.save()
                driver.rent = float(driver.rent) + float(rent_agreement_details['rent'])
                driver.paid = float(driver.paid) + float(rent_agreement_details['paid'])
                driver.balance = float(driver.rent) - float(driver.paid)
                driver.save()
                vehicle.is_available = False
                vehicle.save()
                res = {
                    'result': 'ok',
                    'agreement_id': rent_agreement.id,
                }
                status = 200
            except Exception as ex:
                print str(ex)
                res = {
                    'result': 'error',
                }
                status = 200
            response = simplejson.dumps(res)

            return HttpResponse(response, status=status, mimetype='application/json')

class ReceiveCarView(View):

    def get(self, request, *args, **kwargs):

        receipt_no = ReceiveCar.objects.aggregate(Max('id'))['id__max']
        if not receipt_no:
            receipt_no = 1
        else:
            receipt_no = receipt_no + 1
    
        context = {
            'receipt_no': receipt_no,
        }

        return render(request, 'receive_car.html', context)
    def post(self, request, *args, **kwargs):

        receive_car_details = ast.literal_eval(request.POST['receipt_car'])
        try:
            receive_car, created = ReceiveCar.objects.get_or_create(receipt_no=receive_car_details['receipt_no'])
            rent_agreement = RentAgreement.objects.get(id=receive_car_details['agreement_id'])
            receive_car.rent_agreement = rent_agreement
            receive_car.petrol = receive_car_details['petrol']
            receive_car.returning_petrol = receive_car_details['returning_petrol']
            vehicle = rent_agreement.vehicle
            vehicle.petrol = receive_car_details['returning_petrol']
            vehicle.save()
            receive_car.fine = receive_car_details['fine']
            receive_car.extra_charge = receive_car_details['extra_charge']
            receive_car.credit_card_no = receive_car_details['credit_card_no']
            receive_car.cheque_no = receive_car_details['cheque_no']
            receive_car.total_amount = receive_car_details['total_amount']
            receive_car.paid = receive_car_details['paid']
            receive_car.reduction = receive_car_details['reduction']
            receive_car.notes = receive_car_details['notes']
            receive_car.new_meter_reading = receive_car_details['meter_reading']
            receive_car.leaving_petrol = receive_car_details['returning_petrol']
            receive_car.salik_charges = receive_car_details['salik_charges']
            receive_car.receipt_datetime = utc.localize(datetime.strptime(receive_car_details['receipt_date'], '%d/%m/%Y %I:%M%p'))

            receive_car.returning_date_time = utc.localize(datetime.strptime(receive_car_details['returning_date'], '%d/%m/%Y %I:%M%p'))
            receive_car.save()
            driver = rent_agreement.driver
            driver.rent = float(driver.rent) - float(rent_agreement.rent)
            driver.rent = float(driver.rent) + float(receive_car.total_amount)
            driver.paid = float(driver.paid) + float(receive_car.paid)
            driver.balance = float(driver.rent) - float(driver.paid)
            driver.save() 
            vehicle = rent_agreement.vehicle
            vehicle.meter_reading = receive_car.new_meter_reading
            # if receive_car_details['balance'] == 0:
            vehicle.is_available = True
            rent_agreement.is_completed = True
            rent_agreement.save()
                
            vehicle.save()

            res = {
                'result': 'ok',
                'receipt_id': receive_car.id,
            }
            status = 200
        except Exception as ex:
            print str(ex)
            res = {
                'result': 'error',
            }
            status = 500
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')

class AgreementDetails(View):

    def get(self, request, *args, **kwargs):

        agreement_no = request.GET.get('agreement_no', '')
        # current_date = datetime.now() Generate native error
        current_date = timezone.now()
        try:
            agreements = RentAgreement.objects.filter(is_completed=False, agreement_no__startswith=agreement_no)
            whole_agreements = RentAgreement.objects.filter(is_completed=True)
            whole_rent_agreements = RentAgreement.objects.filter(agreement_no__startswith=agreement_no)
        except Exception as ex:
            print "************************************"
            print str(ex)
        ctx_agreements = []
        ctx_receival_details = []
        ctx_whole_agreements = []
        ctx_rent_agreements = []
        if request.is_ajax():
            if agreements.count() > 0:
                for agreement in agreements:
                    print agreement.receivecar_set.all().count()
                    if agreement.receivecar_set.all().count() > 0:
                        ctx_receival_details.append({
                            'receipt_no': agreement.receivecar_set.all()[0].receipt_no if agreement.receivecar_set.all().count() > 0 else '',
                            'date': agreement.receivecar_set.all()[0].receipt_datetime.strftime('%d/%m/%Y') if agreement.receivecar_set.all().count() > 0 and agreement.receivecar_set.all()[0].receipt_datetime else '',
                            'total_amount': agreement.receivecar_set.all()[0].total_amount if agreement.receivecar_set.all().count() > 0 else '',
                            'deposit': agreement.paid,
                            'new_meter_reading': agreement.receivecar_set.all()[0].new_meter_reading if agreement.receivecar_set.all().count() > 0 else '',
                            'fine': agreement.receivecar_set.all()[0].fine if agreement.receivecar_set.all().count() > 0 else '',
                            # 'damage': agreement.receivecar_set.all()[0].accident_passable if agreement.receivecar_set.all().count() > 0 else '',
                            'petrol': agreement.receivecar_set.all()[0].petrol if agreement.receivecar_set.all().count() > 0 else '',
                            'extra_charge': agreement.receivecar_set.all()[0].extra_charge if agreement.receivecar_set.all().count() > 0 else '',
                            'reduction': agreement.receivecar_set.all()[0].reduction if agreement.receivecar_set.all().count() > 0 else '',
                            'paid': agreement.receivecar_set.all()[0].paid if agreement.receivecar_set.all().count() > 0 else '',
                            # 'vehicle_scratch': agreement.receivecar_set.all()[0].vehicle_scratch if agreement.receivecar_set.all().count() > 0 else '',
                            'petrol_on_return': agreement.receivecar_set.all()[0].returning_petrol if agreement.receivecar_set.all().count() > 0 else '',
                        })
                    late_message = ''
                    if agreement.end_date_time:
                        if agreement.end_date_time < current_date:
                            late_message = 'Late Receival' 

                    ctx_agreements.append({
                        'id': agreement.id,
                        'agreement_no': agreement.agreement_no,
                        # 'client': agreement.client.name if agreement.client else '',
                        'vehicle_no': agreement.vehicle.vehicle_no if agreement.vehicle else '',
                        'rent': agreement.rent,
                        'date': agreement.agreement_date.strftime('%d/%m/%Y') if agreement.agreement_date else '',
                        'begining_date': agreement.starting_date_time.strftime('%d/%m/%Y') if agreement.starting_date_time else '',
                        'begining_time': agreement.starting_date_time.strftime('%I:%M%p') if agreement.starting_date_time else '',
                        'end_date': agreement.end_date_time.strftime('%d/%m/%Y') if agreement.end_date_time else '',
                        'end_time': agreement.end_date_time.strftime('%I:%M%p') if agreement.end_date_time else '',
                        'license_no': agreement.driver.driver_license_no if agreement.driver else '',
                        'license_type': agreement.driver.license_type if agreement.driver else '',
                        'license_date': agreement.driver.driver_license_issue_date.strftime('%d/%m/%Y') if agreement.driver else '',
                        'passport_no': agreement.driver.driver_passport_no if agreement.driver else '',
                        'place_of_issue': agreement.driver.place_of_issue if agreement.driver else '', 
                        'vehicle_condition': agreement.vehicle.vehicle_condition if agreement.vehicle else '',
                        'meter_reading': agreement.vehicle.meter_reading if agreement.vehicle else '',
                        'insurance_value': agreement.vehicle.insuranse_value if agreement.vehicle else '',
                        'insurance_type': agreement.vehicle.type_of_insuranse if agreement.vehicle else '',
                        'plate_no': agreement.vehicle.plate_no if agreement.vehicle else '',
                        'driver_name': agreement.driver.driver_name if agreement.driver else '',
                        'driver_passport_no': agreement.driver.driver_passport_no if agreement.driver else '',
                        'sponsar_name': agreement.driver.sponsar_name if agreement.driver else '',
                        'paid': agreement.paid,
                        'damage': agreement.accident_passable if agreement.accident_passable else 0,
                        'vehicle_scratch': agreement.vehicle_scratch if agreement.vehicle_scratch else 0,
                        'late_message': late_message,
                        'petrol': agreement.leaving_petrol,
                        'receival_details': ctx_receival_details,
                    })
                    ctx_receival_details = []
            for agreement in whole_agreements:
                if agreement.receivecar_set.all().count() > 0:
                    ctx_receival_details.append({
                        'id': agreement.receivecar_set.all()[0].id if agreement.receivecar_set.all().count() > 0 else '',
                        'receipt_no': agreement.receivecar_set.all()[0].receipt_no if agreement.receivecar_set.all().count() > 0 else '',
                        'receipt_date': agreement.receivecar_set.all()[0].receipt_datetime.strftime('%d/%m/%Y') if agreement.receivecar_set.all().count() and agreement.receivecar_set.all()[0].receipt_datetime else '',
                        'total_amount': agreement.receivecar_set.all()[0].total_amount if agreement.receivecar_set.all().count() > 0 else '',
                        'deposit': agreement.paid,
                        'meter_reading': agreement.receivecar_set.all()[0].new_meter_reading if agreement.receivecar_set.all().count() > 0 else '',
                        'fine': agreement.receivecar_set.all()[0].fine if agreement.receivecar_set.all().count() > 0 else '',
                        # 'accident_passable': agreement.receivecar_set.all()[0].accident_passable if agreement.receivecar_set.all().count() > 0 else '',
                        'petrol': agreement.receivecar_set.all()[0].petrol if agreement.receivecar_set.all().count() > 0 else '',
                        'extra_charge': agreement.receivecar_set.all()[0].extra_charge if agreement.receivecar_set.all().count() > 0 else '',
                        'reduction': agreement.receivecar_set.all()[0].reduction if agreement.receivecar_set.all().count() > 0 else '',
                        'paid': agreement.receivecar_set.all()[0].paid if agreement.receivecar_set.all().count() > 0 else '',
                        'credit_card_no': agreement.receivecar_set.all()[0].credit_card_no if agreement.receivecar_set.all().count() > 0 else '',
                        'cheque_no': agreement.receivecar_set.all()[0].cheque_no if agreement.receivecar_set.all().count() > 0 else '',
                    })
            
                ctx_whole_agreements.append({
                    'id': agreement.id,
                    'agreement_no': agreement.agreement_no,
                    # 'client': agreement.client.name if agreement.client else '',
                    'vehicle_no': agreement.vehicle.vehicle_no if agreement.vehicle else '',
                    'rent': agreement.rent,
                    'date': agreement.agreement_date.strftime('%d/%m/%Y'),
                    'begining_date': agreement.starting_date_time.strftime('%d/%m/%Y'),
                    'begining_time': agreement.starting_date_time.strftime('%I:%M%p'),
                    'end_date': agreement.end_date_time.strftime('%d/%m/%Y'),
                    'end_time': agreement.end_date_time.strftime('%I:%M%p'),
                    'license_no': agreement.driver.driver_license_no if agreement.driver else '',
                    'license_type': agreement.driver.license_type if agreement.driver else '',
                    'license_date': agreement.driver.driver_license_issue_date.strftime('%d/%m/%Y') if agreement.driver else '',
                    'passport_no': agreement.driver.driver_passport_no if agreement.driver else '',
                    'place_of_issue': agreement.driver.place_of_issue if agreement.driver else '', 
                    'vehicle_condition': agreement.vehicle.vehicle_condition if agreement.vehicle else '',
                    'meter_reading': agreement.vehicle.meter_reading if agreement.vehicle else '',
                    'insurance_value': agreement.vehicle.insuranse_value if agreement.vehicle else '',
                    'insurance_type': agreement.vehicle.type_of_insuranse if agreement.vehicle else '',
                    'plate_no': agreement.vehicle.plate_no if agreement.vehicle else '',
                    'driver_name': agreement.driver.driver_name if agreement.driver else '',
                    'driver_passport_no': agreement.driver.driver_passport_no if agreement.driver else '',
                    'sponsar_name': agreement.driver.sponsar_name if agreement.driver else '',
                    'paid': agreement.paid,
                    'damage': agreement.accident_passable if agreement.accident_passable else '',
                    'vehicle_scratch': agreement.vehicle_scratch if agreement.vehicle_scratch else 0,
                    'late_message': 'Late receival' if agreement.end_date_time < current_date else 0,
                    'receival_details': ctx_receival_details,
                })
                ctx_receival_details = []
            for agreement in whole_rent_agreements:
                late_message = ''
                if agreement.end_date_time:
                    if agreement.end_date_time < current_date:
                        late_message = 'Late Receival'
                ctx_rent_agreements.append({
                    'id': agreement.id,
                    'agreement_no': agreement.agreement_no,
                    # 'client': agreement.client.name if agreement.client else '',
                    'vehicle_no': agreement.vehicle.vehicle_no if agreement.vehicle else '',
                    'rent': agreement.rent,
                    'date': agreement.agreement_date.strftime('%d/%m/%Y') if agreement.agreement_date else '',
                    'begining_date': agreement.starting_date_time.strftime('%d/%m/%Y') if agreement.starting_date_time else '',
                    'begining_time': agreement.starting_date_time.strftime('%I:%M%p ') if agreement.starting_date_time else '',
                    'end_date': agreement.end_date_time.strftime('%d/%m/%Y') if agreement.end_date_time else '',
                    'end_time': agreement.end_date_time.strftime('%I:%M%p ') if agreement.end_date_time else '',
                    'license_no': agreement.driver.driver_license_no if agreement.driver else '',
                    'license_type': agreement.driver.license_type if agreement.driver else '',
                    'license_date': agreement.driver.driver_license_issue_date.strftime('%d/%m/%Y') if agreement.driver else '',
                    'passport_no': agreement.driver.driver_passport_no if agreement.driver else '',
                    'place_of_issue': agreement.driver.place_of_issue if agreement.driver else '', 
                    'vehicle_condition': agreement.vehicle.vehicle_condition if agreement.vehicle else '',
                    'meter_reading': agreement.vehicle.meter_reading if agreement.vehicle else '',
                    'insurance_value': agreement.vehicle.insuranse_value if agreement.vehicle else '',
                    'insurance_type': agreement.vehicle.type_of_insuranse if agreement.vehicle else '',
                    'plate_no': agreement.vehicle.plate_no if agreement.vehicle else '',
                    'driver_name': agreement.driver.driver_name if agreement.driver else '',
                    'driver_passport_no': agreement.driver.driver_passport_no if agreement.driver else '',
                    'sponsar_name': agreement.driver.sponsar_name if agreement.driver else '',
                    'paid': agreement.paid,
                    'late_message': late_message,
                    'damage': agreement.accident_passable if agreement.accident_passable else 0,
                    'vehicle_scratch': agreement.vehicle_scratch if agreement.vehicle_scratch else 0,
                })
            
            res = {
                'result': 'ok',
                'agreements': ctx_agreements,
                'whole_agreements': ctx_whole_agreements,
                'rent_agreements': ctx_rent_agreements,
            }
            status = 200
            response = simplejson.dumps(res)

            return HttpResponse(response, status=status, mimetype='application/json')

class PrintRentAgreement(View):

    def get(self, request, *args, **kwargs):

        rent_agreement_id = request.GET.get('rent_agreement_id', '')
        if not rent_agreement_id:
            return render(request, 'print_rent_agreement.html', {})
        else:
            rent_agreement = RentAgreement.objects.get(id=rent_agreement_id)

            response = HttpResponse(content_type='application/pdf')
            p = canvas.Canvas(response, pagesize=(1000, 1200))

            status_code = 200

            y = 1200
            
            p.setFont("Helvetica-Bold", 30)
            p.setFillColor(green)
            p.drawString(50, 1160, 'Golden Cup Rent A Car')
            p.setFillColor(black)

            p.setFont("Helvetica", 12)
            p.drawString(50, 1120, 'Tel : 02-6266634 , Mob : 055-4087528, 055-3020434 , P.O.Box : 32900')
            p.drawString(50, 1095, 'Fax : 02-6420741')
            p.drawString(50, 1070, 'Old Passport Road , Abu Dhabi - UAE')
            p.setFont("Helvetica", 16)
            p.drawString(50, 1010, 'Date : ......................')
            p.setFont("Helvetica", 13)
            p.drawString(90, 1015, rent_agreement.agreement_date.strftime('%d/%m/%Y'))
            p.drawString(820, 1015, rent_agreement.agreement_date.strftime('%d/%m/%Y'))
            p.setFont("Helvetica-Bold", 15)
            p.drawString(410, 1050, 'RENTAL AGREEMENT')
            p.line(50, 1000, 950, 1000)
            p.line(500, 1000, 500, 150)
            p.line(250, 1000, 250, 900)
            p.line(50, 950, 950, 950)
            p.line(50, 900, 950, 900)
            p.line(50, 850, 950, 850)
            p.line(375,900, 375, 850)
            p.line(50, 800, 950, 800)
            # p.line(375, 750, 375, 750)
            p.line(50, 750, 950, 750)
            p.line(50, 700, 950, 700)
            p.line(50, 650, 950, 650)
            p.line(50, 600, 950, 600)
            p.line(250, 600, 250, 750)
            # p.line(750, 650, 750, 750)
            p.line(750, 900, 750, 1000)
            p.line(750, 750, 750, 800)
            # p.line(750, 800, 750, 850)

            p.line(250, 300, 250, 750)
            p.line(300, 850, 300, 800)
            p.line(50, 500, 500, 500)
            p.line(50, 550, 500, 550)
            p.line(50, 450, 500, 450)
            p.line(50, 400, 500, 400)
            p.line(500, 550, 950, 550)
            p.line(500, 500, 950, 500)
            p.line(50, 350, 500, 350)
            p.line(50, 300, 500, 300)
            p.line(50, 250, 500, 250)
            p.line(250, 300, 250, 250)

            y = 980
            p.drawString(50, y, 'Vehicle Type')
            p.drawString(260, y, 'Reg. No.')
            p.drawString(50, y - 50, 'Vehicle Make')
            p.drawString(260, y - 50, 'Vehicle Colour')
            p.drawString(80, y - 100, 'Leaving Date')
            p.drawString(400, y - 100, 'Time')
            p.drawString(60, y - 157, 'Meter Reading on Leaving')
            p.drawString(310, y - 157, 'Petrol on Leaving')
            p.drawString(50, y - 200, 'Expecting Returning Date')
            p.drawString(400, y - 200, 'Time')

            p.setFont("Helvetica", 15)
            p.drawString(510, y - 15, 'Passport Issued Date: ')
            p.drawString(760, y - 15, 'Issued Place: ')
            p.drawString(510, y - 60, 'Date of Birth: ')
            p.drawString(760, y - 60, 'Tel No: ')
            p.drawString(510, y - 170, 'License Date & Place of Issue: ')
            p.drawString(560, y - 300, 'Emirates Id: ')
            p.drawString(560, y - 250, 'License Type: ')
            p.drawString(510, y - 120, 'Address:')
            p.drawString(760, y - 110, 'Agreement Type')
            p.drawString(510, y - 210, 'License Expiry Date:')
            p.drawString(760, y - 210, 'Client Identity:')

            p.drawString(100, y - 460, 'Rent Amount')
            p.drawString(100, y - 510, 'Total Amount')
            p.drawString(100, y - 560, 'Paid')
            p.drawString(100, y - 610, 'Balance')
            p.drawString(100, y - 660, 'Accident Passable')
            p.drawString(100, y - 700, 'Vehicle Scrtach')
            p.drawString(50, y - 410, 'Rental Entitled in KM')
            p.drawString(250, y - 410, 'Liable to Pay in KM')

            p.drawString(50, y - 250, 'Driver Name')
            p.drawString(260, y - 250, 'License No')
            p.drawString(50, y - 300, 'Passport No')
            p.drawString(260, y - 300, 'Nationality')

            p.drawString(50, y - 350, 'Sponsar Name')
            p.drawString(260, y - 350, 'Sponsar Tel.')
            p.drawString(560, y - 350, 'Sponsar Address')
            p.drawString(560, y - 400, 'Driver Working Address')
            p.drawString(560, y - 450, 'Driver Tel. No ( Working )')


            p.setFont("Helvetica", 13)
            vehicle = rent_agreement.vehicle
            p.drawString(100, 960, vehicle.vehicle_type_name.vehicle_type_name if vehicle and vehicle.vehicle_type_name else '')
            p.drawString(300, 960, rent_agreement.agreement_no)
            p.drawString(100, 910, str(vehicle.vehicle_make) if vehicle else '')
            p.drawString(300, 910, str(vehicle.vehicle_color) if vehicle else '')
            p.drawString(200, 860, rent_agreement.starting_date_time.strftime('%d/%m/%Y'))
            p.drawString(400, 860, rent_agreement.starting_date_time.strftime('%I:%M %p'))
            p.drawString(150, 810, str(rent_agreement.leaving_meterreading if rent_agreement.leaving_meterreading else ''))
            p.drawString(380, 810, str(rent_agreement.leaving_petrol))
            p.drawString(200, 760, rent_agreement.end_date_time.strftime('%d/%m/%Y'))
            p.drawString(400, 760, rent_agreement.end_date_time.strftime('%I:%M %p'))

            p.drawString(660, 965, rent_agreement.driver.date_of_passport_issue.strftime('%d/%m/%Y') if rent_agreement.driver and rent_agreement.driver.date_of_passport_issue else '')
            p.drawString(860, 965, rent_agreement.driver.place_of_issue if rent_agreement.driver else '')
            p.drawString(600, 920, rent_agreement.driver.driver_dob.strftime('%d/%m/%Y') if rent_agreement.driver and rent_agreement.driver.driver_dob else '')
            p.drawString(850, 920, rent_agreement.driver.driver_phone if rent_agreement.driver else '')
            p.drawString(720, 810, (rent_agreement.driver.driver_license_issue_date.strftime('%d/%m/%Y') if rent_agreement.driver and rent_agreement.driver.driver_license_issue_date else '') + ' , ')
            p.drawString(795, 810, rent_agreement.driver.driver_license_issue_place if rent_agreement.driver else '')
            p.drawString(580, 660, rent_agreement.driver.emirates_id if rent_agreement.driver else '')
            p.drawString(580, 710, rent_agreement.driver.license_type if rent_agreement.driver else '')
            p.drawString(580, 860, rent_agreement.driver.driver_address.replace('\n', ' ') if rent_agreement.driver and rent_agreement.driver.driver_address else '')
            p.drawString(820, 855, rent_agreement.rent_type if rent_agreement else 'None')
            p.drawString(650, 770, rent_agreement.driver.driver_license_expiry_date.strftime('%d/%m/%Y') if rent_agreement.driver and rent_agreement.driver.driver_license_expiry_date else '')
            p.drawString(860, 770, rent_agreement.client_identity if rent_agreement.client_identity else '')
            
            p.drawString(130, 710, rent_agreement.driver.driver_name)
            p.drawString(320, 710, rent_agreement.driver.driver_nationality)
            p.drawString(130, 660, rent_agreement.driver.driver_passport_no if rent_agreement.driver.driver_passport_no else '')
            p.drawString(320, 660, rent_agreement.driver.driver_nationality)

            p.drawString(140, 610, rent_agreement.driver.sponsar_name)
            p.drawString(340, 610, rent_agreement.driver.sponsar_phone)
            p.drawString(550, 610, rent_agreement.driver.sponsar_address)


            p.drawString(260, 520, str(rent_agreement.rent))
            p.drawString(260, 470, str(rent_agreement.total_amount))
            p.drawString(260, 420, str(rent_agreement.paid))
            p.drawString(260, 370, str(float(rent_agreement.total_amount) - float(rent_agreement.paid)))
            p.drawString(260, 320, str(rent_agreement.accident_passable))
            p.drawString(260, 280, str(rent_agreement.vehicle_scratch))
            p.drawString(200, 570, str(rent_agreement.rental_entitled_in_km))
            p.drawString(390, 570, str(rent_agreement.liable_to_pay_in_km))
            p.drawString(610, 560, str(rent_agreement.driver.driver_working_address))
            p.drawString(610, 510, str(rent_agreement.driver.driver_working_ph))

            p.drawString(60, 180, """This vehicle cann't be taken outside the UAE without prior permission""")
            p.drawString(60, 160, """ of the owner in writing""")
            p.drawString(503, 400, """I the undersigned agree to rent from the owner the above mentioned vehcile""")
            p.drawString(503, 380, """for the period set our herein. I have read the terms and conditions det out on""")
            p.drawString(503, 360, """the reverse of this agreement between my self and the owner. I certify that """)
            p.drawString(503, 340, """the particualrs which i have given are true""")
            p.drawString(503, 280, """ In the Event of any Accident The Renter is Liable to pay Hire.""")
            p.drawString(503, 180,'SIGNATURE :.........................................................................')
            
            p.setFont('Arabic-normal', 18)
            date_arabic =  '.................:'+ arabic_text_date[::-1]
            p.drawString(820, 1010, date_arabic)
            arabic_text_rent_agreement = u'عقد تأجير'
            p.drawString(610, 1050, arabic_text_rent_agreement[::-1])
            p.setFont('Arabic-normal', 17)
            arabic_text_vehicle_type = u'نوع السيارات'
            p.drawString(170, 980, arabic_text_vehicle_type[::-1])
            arabic_text_reg_no = u'رقم اللوحة'
            p.drawString(350, 980, arabic_text_reg_no[::-1])
            arabic_text_vehicle_make = u'طاراز السيارات'
            p.drawString(160, 930, arabic_text_vehicle_make[::-1])
            arabic_text_vehicle_color = u'لون السيارات'
            p.drawString(370, 930, arabic_text_vehicle_color[::-1])
            arabic_text_leaving_date = u'تاريخ مغادرة السيارات'
            p.drawString(240, 880, arabic_text_leaving_date[::-1])
            p.drawString(440, 880, arabic_text_time[::-1])
            arabic_text_meter_reading_leaving = u'قراءة العداد عند مغادرة السيارات'
            p.drawString(60, 840, arabic_text_meter_reading_leaving[::-1])
            arabic_text = u'البنزين على ترك'
            p.drawString(310, 840, arabic_text[::-1])
            arabic_text_exp_return_date = u'تتوقع عودته التسجيل'
            p.drawString(250, 780, arabic_text_exp_return_date[::-1])
            p.drawString(440, 780, arabic_text_time[::-1])
            p.drawString(510, 987, arabic_text_passport_issue_date[::-1])
            p.drawString(760, 987, arabic_text_issued_place[::-1])
            p.drawString(510, 937, arabic_text_dob[::-1])
            p.drawString(760, 937, arabic_text_tel[::-1])
            arabic_text_date_place_issue = u'تاريخ ومكان الإصدار'
            p.drawString(510, 830, arabic_text_date_place_issue[::-1])
            p.drawString(690,680, arabic_text_emirates_id[::-1])
            p.drawString(670, 730, arabic_text_license_type[::-1])
            p.drawString(510, 880, arabic_text_address[::-1])
            agreement_type = u'نوع اتفاق'
            p.drawString(810, 885, agreement_type[::-1])
            arabic_text_license_expiry_date = u'الترخيص تاريخ انتهاء الصلاحية'
            p.drawString(510, 790, arabic_text_license_expiry_date[::-1])
            arabic_text_client_identity = u'الهوية عميل'
            p.drawString(760, 790, arabic_text_client_identity[::-1])
            arabic_text_amount = u'مبلغ'
            p.drawString(100, 540, arabic_text_amount[::-1])
            p.drawString(100, 490, arabic_text_total_amount[::-1])
            p.drawString(100, 440, arabic_text_paid[::-1])
            p.drawString(100, 390, arabic_text_balance[::-1])
            p.drawString(100, 340, arabic_text_vehicle_scratch[::-1])
            p.drawString(100, 260, arabic_text_accident[::-1])
            rental_in_km = u'تأجير بعنوان في الكيلومتر'
            p.drawString(50, 590, rental_in_km[::-1])
            liable_to_pay_in_km = u'مسؤولا عن دفع في الكيلومتر'
            p.drawString(260, 590, liable_to_pay_in_km[::-1])

            p.drawString(150, 730, arabic_text_driver_name[::-1])
            
            p.drawString(350, 730, arabic_text_license_no[::-1])
            
            p.drawString(150, 680, arabic_text_passport_no[::-1])
            
            p.drawString(350, 680, arabic_text_nationality[::-1])
            
            p.drawString(150, 630, arabic_text_sponsar_name[::-1])
            
            p.drawString(350, 630, arabic_text_sponsar_tel[::-1])
            
            p.drawString(760, 630, arabic_text_sponsar_address[::-1])
            p.drawString(760, 580, arabic_text_address[::-1])
            p.drawString(760, 530, arabic_text_tel[::-1])
            
            p = draw_heading(p) 

            p.setFont('Arabic-normal', 13)
            arabic_text = u'أناالموقع ادناه اوافق على استئجار السياراة المزكورة اعلاه من المالك وللمعدة المشرليها كما وأصرح'
            p.drawString(503, 470, arabic_text[::-1])
            arabic_text = u'بأننى قرأت الشروط المدنة على ظهر هذه الا تفاقة المعقودة بينى وبين المالك كما واقربأن البيانات التى'
            p.drawString(503, 450, arabic_text[::-1])
            arabic_text = u'اعطيتها فى صحية'
            p.drawString(850, 430, arabic_text[::-1])
            arabic_text = u'بدفع للستأجر قيمة الوقت التانج عن الحادث خروج السيارات من الكراج '
            p.drawString(503, 300, arabic_text[::-1])
            arabic_text = u'لا يجوز اخز السيارات خارج حدود دولة الامارت العربية للمتحدة بدون اذن خطي مسبق من قبل المالك'
            p.drawString(60, 210, arabic_text[::-1])

            p.showPage()
            p.save()

            return response

class AddDriver(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'add_driver.html', {})

    def post(self, request, *args, **kwargs):

        if request.is_ajax():

            status = 200
            ctx_driver = []
            driver_details = ast.literal_eval(request.POST['driver_details'])
            try:
                try:
                    driver = Driver.objects.get(driver_phone=driver_details['home_ph_no'])
                    message = 'Driver with this Phone No is already existing'
                except Exception as ex:
                    print str(ex)
                    
                    driver = Driver.objects.get(driver_license_no=driver_details['license_no'])
                    message = 'Driver with this License No is already existing'
                    print message
                res = {
                    'result': 'error',
                    'message': message,
                }
            except Exception as ex:
                print str(ex)
                driver = Driver.objects.create(driver_phone=driver_details['home_ph_no'], driver_license_no=driver_details['license_no'])
                driver.driver_name = driver_details['name']  

                driver.driver_address = request.POST['home_address'] 
                driver.driver_nationality = driver_details['nationality']
                # driver.driver_license_no = driver_details['license_no']
                driver.driver_license_issue_date = datetime.strptime(driver_details['date_of_license_issue'], '%d/%m/%Y')
                driver.driver_license_issue_place = driver_details['issued_place']
                driver.driver_license_expiry_date = datetime.strptime(driver_details['expiry_date'], '%d/%m/%Y')
                driver.driver_dob = datetime.strptime(driver_details['dob'], '%d/%m/%Y')
                driver.sponsar_name = driver_details['sponsar_name']
                driver.sponsar_address = request.POST['sponsar_address']
                driver.sponsar_phone = driver_details['sponsar_ph']
                driver.driver_working_address = request.POST['driver_working_address']
                driver.driver_working_ph = driver_details['working_tel_no']
                driver.license_type = driver_details['license_type']
                if driver_details['passport_issued_date']:
                    driver.date_of_passport_issue = datetime.strptime(driver_details['passport_issued_date'], '%d/%m/%Y')
                driver.place_of_issue = driver_details['place_of_issue']
                driver.emirates_id = driver_details['emirates_id']
                driver.save()
                ctx_driver.append({
                    'id': driver.id,
                    'driver_name': driver.driver_name,
                    'driver_address': driver.driver_address,
                    'driver_phone': driver.driver_phone,
                    'driver_nationality': driver.driver_nationality,
                    'driver_license_no': driver.driver_license_no,
                    'driver_license_issue_date': driver.driver_license_issue_date.strftime('%d/%m/%Y') if driver.driver_license_issue_date else '',
                    'driver_license_issue_place': driver.driver_license_issue_place,
                    'driver_license_expiry_date': driver.driver_license_expiry_date.strftime('%d/%m/%Y') if driver.driver_license_expiry_date else '',
                    'driver_dob': driver.driver_dob.strftime('%d/%m/%Y') if driver.driver_dob else '',
                    'sponsar_name': driver.sponsar_name,
                    'sponsar_address': driver.sponsar_address,
                    'sponsar_phone': driver.sponsar_phone,
                    'passport_no': driver.driver_passport_no,
                    'driver_working_address': driver.driver_working_address,
                    'working_tel_no': driver.driver_working_ph,
                    'license_type': driver.license_type,
                    'place_of_issue': driver.place_of_issue,
                    'emirates_id': driver.emirates_id,
                    'passport_issued_date': driver.date_of_passport_issue.strftime('%d/%m/%Y') if driver.date_of_passport_issue else '',
                })
                res = {
                    'result': 'ok',
                    'driver_data': ctx_driver,
                }

            response = simplejson.dumps(res)

            return HttpResponse(response, status=status, mimetype='application/json')

class DriversList(View):

    def get(self, request, *args, **kwargs):

        ctx_drivers = []
        if request.is_ajax():
            status = 200
            drivers = Driver.objects.filter(driver_name__istartswith=request.GET.get('driver_name', ''))

            for driver in drivers:
                ctx_drivers.append({
                    'id': driver.id,
                    'name': driver.driver_name + ' - ' + driver.driver_license_no,
                    'driver_name': driver.driver_name,
                    'driver_phone': driver.driver_phone,
                    'driver_address': driver.driver_address,
                    'driver_nationality': driver.driver_nationality,
                    'passport_no': driver.driver_passport_no,
                    'driver_license_no': driver.driver_license_no,
                    'driver_license_issue_date': driver.driver_license_issue_date.strftime('%d/%m/%Y') if driver.driver_license_issue_date else '',
                    'driver_license_issue_place': driver.driver_license_issue_place,
                    'driver_license_expiry_date': driver.driver_license_expiry_date.strftime('%d/%m/%Y') if driver.driver_license_expiry_date else '',
                    'driver_dob': driver.driver_dob.strftime('%d/%m/%Y') if driver.driver_dob else '',
                    'sponsar_name': driver.sponsar_name,
                    'sponsar_address': driver.sponsar_address,
                    'sponsar_phone': driver.sponsar_phone,
                    'driver_working_address': driver.driver_working_address,
                    'working_tel_no': driver.driver_working_ph,
                    'license_type': driver.license_type,
                    'place_of_issue': driver.place_of_issue,
                    'emirates_id': driver.emirates_id,
                    'passport_issued_date': driver.date_of_passport_issue.strftime('%d/%m/%Y') if driver.date_of_passport_issue else '',
                })
            res = {
                'result': 'ok',
                'drivers': ctx_drivers,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        else:
            drivers = Driver.objects.all().order_by('id')
            context = {
                'drivers': drivers,
            }
            return render(request, 'drivers.html', context)

class PrintReceiptCar(View):

    def get(self, request, *args, **kwargs):
        receipt_car_id = request.GET.get('receipt_car_id', '')
        if not receipt_car_id:
            return render(request, 'print_receival_car_details.html', {})
        else:
            response = HttpResponse(content_type='application/pdf')
            p = canvas.Canvas(response, pagesize=(1000, 1200))
            receive_car = ReceiveCar.objects.get(id = int(receipt_car_id))
            
            status_code = 200

            y = 1200
            p.setFont("Helvetica-Bold", 30)
            p.setFillColor(green)
            p.drawString(50, 1160, 'Golden Cup Rent A Car')
            p.setFillColor(black) 

            # p.drawImage(path, 70, 1065, width=30*cm, height=3*cm, preserveAspectRatio=True)

            p.setFont("Helvetica", 12)
            p.drawString(50, 1130, 'Tel : 02-6266634 , Mob : 055-4087528 , P.O.Box : 32900')
            p.drawString(50, 1100, 'Fax : 02-6420741')
            p.drawString(50, 1070, 'Old Passport Road , Abu Dhabi - UAE')
            p.setFont("Helvetica", 16)
            p.drawString(50, 1010, 'Date : ......................')
            p.setFont("Helvetica", 13)

            p.drawString(100, 1015,receive_car.receipt_datetime.strftime('%d/%m/%Y') if receive_car.receipt_datetime else '')
            p.drawString(830, 1015,receive_car.receipt_datetime.strftime('%d/%m/%Y') if receive_car.receipt_datetime else '')
            p.setFont("Helvetica-Bold", 15)
            p.drawString(410, 1010, 'RENTAL CAR RECEIPT')
            p.line(50,1000,950,1000)
            p.line(500,1000,500,130)
            p.line(50, 950, 950,950)
            p.line(50, 900, 950, 900)
            p.line(50, 850, 950, 850)
            p.line(50, 800, 950, 800)
            p.line(50, 750, 950, 750)
            p.line(50, 700, 950, 700)
            p.line(50, 650, 950, 650)
            p.line(250, 700, 250, 650)
            p.line(250, 600, 250, 650)
            p.line(250, 550, 250, 600)
            p.line(50, 600, 950, 600)
            p.line(50, 550, 950, 550)
            p.line(50, 500, 950, 500)
            p.line(500, 450, 950, 450)
            p.line(500, 410, 950, 410)
            p.line(500, 370, 950, 370)
            p.line(500, 330, 950, 330)
            p.line(500, 290, 950, 290)
            p.line(500, 250, 950, 250)
            p.line(500, 210, 950, 210)
            p.line(500, 170, 950, 170)
            p.line(500, 130, 950, 130)
            p.line(250, 550, 250, 500)
            # p.line(250, 500, 250, 450)
            p.line(750, 500, 750, 550)
            
            p.line(750, 450, 750, 130)
            p.line(500, 130, 500, 90)
            p.line(750, 130, 750, 90)
            p.line(500, 90, 950, 90)

            p.setFont("Helvetica", 15)
            
            y = 960

            p.drawString(50, y, 'Driver Name: ')
            p.drawString(50, y - 50, 'Nationality: ')
            p.drawString(50, y - 100, 'Passport No: ')
            p.drawString(50, y - 150, 'Address:')
            p.drawString(50, y - 200, 'License No: ')
            p.drawString(50, y - 250, 'License Issue Date - Expiry Date : ')

            p.drawString(510, y, 'Passport Issue Date:')
            p.drawString(510, y - 50, 'Passport Issue Place:')
            p.drawString(510, y - 100, 'Date of Birth: ')
            p.drawString(510, y - 150, 'Tel No: ')
            p.drawString(510, y - 200, 'License Type: ')
            
            p.drawString(510, y - 300, 'Emirates Id: ')
            p.drawString(50, y - 300, 'Leaving Date: ')
            p.drawString(260, y - 300, 'Time: ')
            p.drawString(510, y - 250, 'License Issue Place:')
            p.drawString(50, y - 350, 'Returning Date:')
            p.drawString(260, y - 350, 'Time: ' )
            p.drawString(510, y - 350, 'Tel No.( Working ):')
            p.drawString(510, y - 400, 'Address ( Working ): ')
            # p.drawString(50, y - 400, 'Entering Date:')
            # p.drawString(260, y - 400, 'Time:')

            p.drawString(50, y - 400, 'Plate No: ')
            p.drawString(260, y - 400, 'Car Color: ')
            p.drawString(50, y - 450, 'Vehicle Type: ')
            p.drawString(260, y - 450, 'Made: ')
            p.drawString(510, y - 450, 'Return Meter Reading: ')
            p.drawString(760, y - 450, 'Petrol on Returning ')
            p.drawString(510, y - 500, 'Insurance Value: ')

            p.drawString(760, y - 545, 'Deposit')
            p.drawString(760, y - 580, 'Fine')
            p.drawString(760, y - 620, 'Petrol')
            p.drawString(760, y - 650, 'Extra Charge')
            p.drawString(760, y - 690, 'Reduction')
            p.drawString(760, y - 730, 'Rent')
            p.drawString(750, y - 770, 'Salik Charges')
            p.drawString(750, y - 810, 'Total Amount')
            p.drawString(760, y - 850, 'Balance')

            p.drawString(60, y - 620, "We don't receipt the car in Thursday, Friday the formal holiday")
            p.drawString(60, y - 660, "Acknowledge that I have read the above and reverse method")
            p.drawString(60, y - 700, "terms and conditions and agree to able by them")
            p.drawString(350, y - 780, '....................... Hirer')
            p.drawString(250, y - 840, '..............................Office incharge')

            p.drawString(150, y, receive_car.rent_agreement.driver.driver_name)
            p.drawString(140, y - 50, receive_car.rent_agreement.driver.driver_nationality)
            p.drawString(140, y - 100, receive_car.rent_agreement.driver.driver_passport_no if receive_car.rent_agreement.driver.driver_passport_no else '')
            p.drawString(120, y - 150, receive_car.rent_agreement.driver.driver_address.replace('\n', ' '))

            p.drawString(150, y - 200, receive_car.rent_agreement.driver.driver_license_no)
            p.drawString(280, y - 250, receive_car.rent_agreement.driver.driver_license_issue_date.strftime('%d/%m/%Y') + ' - ' + receive_car.rent_agreement.driver.driver_license_expiry_date.strftime('%d/%m/%Y'))

            p.drawString(660, y, receive_car.rent_agreement.driver.date_of_passport_issue.strftime('%d/%m/%Y') if receive_car.rent_agreement.driver and receive_car.rent_agreement.driver.date_of_passport_issue else '')
            p.drawString(660, y - 50, receive_car.rent_agreement.driver.place_of_issue)
            p.drawString(610, y - 100, receive_car.rent_agreement.driver.driver_dob.strftime('%d/%m/%Y') if receive_car.rent_agreement.driver and receive_car.rent_agreement.driver.driver_dob else '')
            p.drawString(610, y - 150, receive_car.rent_agreement.driver.driver_phone)
            p.drawString(620, y - 200, receive_car.rent_agreement.driver.license_type)
            p.drawString(600, y - 300, receive_car.rent_agreement.driver.emirates_id)
            
            p.drawString(650, y - 250, receive_car.rent_agreement.driver.driver_license_issue_place)
            p.drawString(150, y - 300, receive_car.rent_agreement.starting_date_time.strftime('%d/%m/%Y'))
            p.drawString(300, y - 300, receive_car.rent_agreement.starting_date_time.strftime('%I:%M%p'))
            p.drawString(160, y - 350, receive_car.rent_agreement.end_date_time.strftime('%d/%m/%Y'))
            p.drawString(300, y - 350, receive_car.rent_agreement.end_date_time.strftime('%I:%M%p'))
            p.drawString(650, y - 350, receive_car.rent_agreement.driver.driver_working_ph)
            # p.drawString(150, y - 400, receive_car.receipt_datetime.strftime('%d/%m/%Y') if receive_car.receipt_datetime else '')
            # p.drawString(300, y - 400, receive_car.receipt_datetime.strftime('%I:%M%p') if receive_car.receipt_datetime else '')
            p.drawString(660, y - 400, receive_car.rent_agreement.driver.driver_working_address.replace('\n', ' ') if receive_car.rent_agreement.driver and receive_car.rent_agreement.driver.driver_working_address else '')
            p.drawString(140, y - 400, receive_car.rent_agreement.vehicle.plate_no)
            p.drawString(340, y - 400, str(receive_car.rent_agreement.vehicle.vehicle_color))
            p.drawString(150, y - 450, receive_car.rent_agreement.vehicle.vehicle_type_name.vehicle_type_name if receive_car.rent_agreement.vehicle and receive_car.rent_agreement.vehicle.vehicle_type_name else '')
            p.drawString(330, y - 450, str(receive_car.rent_agreement.vehicle.vehicle_make))
            p.drawString(670, y - 450, str(receive_car.new_meter_reading))
            p.drawString(900, y - 450, receive_car.returning_petrol)
            p.drawString(650, y - 500, str(receive_car.rent_agreement.vehicle.insuranse_value))

            p.drawString(550, y - 545, str(receive_car.rent_agreement.paid))
            p.drawString(550, y - 580, str(receive_car.fine))
            p.drawString(550, y - 620, str(receive_car.petrol))
            p.drawString(550, y - 650, str(receive_car.extra_charge))
            
            p.drawString(550, y - 690, str(receive_car.reduction))
            p.drawString(550, y - 730, str(receive_car.rent_agreement.rent))
            p.drawString(550, y - 770, str(receive_car.salik_charges))
            p.drawString(550, y - 810, str(receive_car.total_amount))
            p.drawString(550, y - 850, str(float(receive_car.total_amount) - (float(receive_car.paid) + float(receive_car.rent_agreement.paid))))

            y = 1010
            p.setFont('Arabic-normal', 18)
            
            date_arabic =  '.................:'+ arabic_text_date[::-1]
            p.drawString(850, y , date_arabic)
            p.drawString(50, y - 30, arabic_text_driver_name[::-1])
            arabic_text = u'الجنسية'
            p.drawString(50, y - 80, arabic_text[::-1])
            arabic_text = u'رقم الجواز'
            p.drawString(50, y - 130, arabic_text[::-1])
            
            p.drawString(50, y - 180, arabic_text_address[::-1])
            arabic_text = u'تاريخ الاصدار الرخصة  - تاريخ الانتهاء'
            p.drawString(50, y - 280, arabic_text[::-1])

            arabic_text_driver_license_no = u'السائق رقم الرخصة'
            p.drawString(50, y - 230, arabic_text_driver_license_no[::-1])

            p.drawString(510, y - 30, arabic_text_passport_issue_date[::-1])
            passport_issue_place = u'جواز سفر العدد مكان'
            p.drawString(510, y - 80, passport_issue_place[::-1])
            
            p.drawString(510, y - 130, arabic_text_dob[::-1])
            
            p.drawString(510, y - 180, arabic_text_tel[::-1])
            p.drawString(510, y - 230, arabic_text_license_type[::-1])
            
            p.drawString(510, y - 330, arabic_text_emirates_id[::-1])
            arabic_text = u'تاريخ مغادرة السيارات '
            p.drawString(50, y - 330, arabic_text[::-1])
            
            p.drawString(260, y - 330, arabic_text_time[::-1])
            arabic_text_license_issue_place = u'العدد الترخيص مكان'
            p.drawString(510, y - 280, arabic_text_license_issue_place[::-1])
            arabic_text = u'تاريخ عودة السيارات' 
            p.drawString(50, y - 380, arabic_text[::-1])
            p.drawString(260, y - 380, arabic_text_time[::-1])
            p.drawString(510, y - 380, arabic_text_tel[::-1])
            p.drawString(510, y - 430, arabic_text_address[::-1])
            # entering_date = u'دخول التسجيل'
            # p.drawString(50, y - 430, entering_date[::-1])
            # p.drawString(260, y - 430, arabic_text_time[::-1])
            plate_no = u'رقم اللوحة'
            p.drawString(50, y - 430, plate_no[::-1])
            arabic_text = u'لون السيارات'
            p.drawString(260, y - 430, arabic_text[::-1])
            arabic_text = u'نوع السيارات'
            p.drawString(50, y - 480, arabic_text[::-1])
            made = u'مصنوع'
            p.drawString(260, y - 480, made[::-1])
            return_meter_reading = u'عودة قراءة العداد'
            p.drawString(510, y - 480, return_meter_reading[::-1])
            petrol_on_return = u'البنزين على العودة'
            p.drawString(760, y - 480, petrol_on_return[::-1])
            insuranse_value = u'القيمة التأمين'
            p.drawString(510, y - 530, insuranse_value[::-1])
            arabic_text_deposit = u'الوديعة'
            p.drawString(760, y - 580, arabic_text_deposit[::-1])
            arabic_text_fine = u'غرامه'
            p.drawString(760, y - 615, arabic_text_fine[::-1])
            arabic_text_petrol = u'بنزين'
            p.drawString(760, y - 655, arabic_text_petrol[::-1])
            arabic_text_extra_charge = u'رسوم إضافية'
            p.drawString(760, y - 715, arabic_text_extra_charge[::-1])
            arabic_text_reduction = u'تخفيض'
            p.drawString(760, y - 755, arabic_text_reduction[::-1])
            rent = u'إيجار'
            p.drawString(760, y - 795, rent[::-1])

            arabic_text = u'الكفيل' 
            p.drawString(420, y - 800, arabic_text[::-1])
            # office in charge
            arabic_text = u'مسؤول المكتب'
            p.drawString(370, y - 870, arabic_text[::-1])
            arabic_text_slalik_changes = u'رسوم سالك'
            p.drawString(845, y - 820, arabic_text_slalik_changes[::-1])
            p.drawString(845, y - 860, arabic_text_total_amount[::-1])
            p.drawString(840, y - 910, arabic_text_balance[::-1])

            p = draw_heading(p)
            # contents
            p.setFont('Arabic-normal', 15)

            content_1 = u'لايتم استلام السيارات يوم الخميس والجمعة والتهانيا والعطال والرسمية والأعياد'
            p.drawString(80, y - 580, content_1[::-1])

            content_2 = u'اقربانني اطلعت على هذه الاتفاقية والشروط المدونة في الخلف وعليها اوقع'

            p.drawString(100, y - 620, content_2[::-1])

            p.showPage()
            p.save()

            return response

class CaseEntry(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'case_entry.html', {})

    def post(self, request, *args, **kwargs):

        if request.is_ajax():

            case_details = ast.literal_eval(request.POST['case_details'])
            driver = Driver.objects.get(id = int(case_details['client_id']))
            vehicle = Vehicle.objects.get(id=case_details['vehicle_id'])
            case = CaseDetail.objects.create(vehicle=vehicle, client=driver)
            case.vehicle_status = case_details['vehicle_status']
            case.rent_agreement_reference_no = case_details['ref_no']
            case.fine_amount = case_details['fine']
            case.type_of_case = case_details['type_of_case']
            case.penality_date = datetime.strptime(case_details['penality_date'], '%d/%m/%Y')
            case.penality_no = case_details['penality_no']
            case.date_author = datetime.strptime(case_details['date_author'], '%d/%m/%Y')
            case.no_author = case_details['no_author']
            case.code_author = case_details['code_author']
            case.save()
            res = {
                'result': 'ok',
            }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')


class RentAgreementDetails(View):

    def get(self, request, *args, **kwargs):
        ctx_client_details = []
        start_date = request.GET.get('start_date', '')
        vehicle_no = request.GET.get('vehicle_no', '')
        rent_agreements = []
        
        if start_date and vehicle_no:
            start = start_date
            start_date = datetime.strptime(start, '%d/%m/%Y')
            start_date = datetime.combine(start_date, dt.time.max)
            end_date = datetime.strptime(start, '%d/%m/%Y')
            end_date = datetime.combine(end_date, dt.time.min)
            
            rent_agreements = RentAgreement.objects.filter(Q(vehicle__vehicle_no__icontains=vehicle_no),Q(starting_date_time__lte=start_date, end_date_time__gte=end_date))
            
        if request.is_ajax():
            res = {
                'result': 'ok',
                'client_name': rent_agreements[0].driver.driver_name if rent_agreements else '',
                'client_id': rent_agreements[0].driver.id if rent_agreements else '',
                'vehicle_id': rent_agreements[0].vehicle.id if rent_agreements else '',
                'ref_no': rent_agreements[0].agreement_no if rent_agreements.count() > 0 else '',
                'vehicle_status': "Outside" if rent_agreements.count() > 0 else "Inside"
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')

class TypeOfCaseList(View):

    def get(self, request, *args, **kwargs):

        type_of_cases = TypeOfCase.objects.all().order_by('id')
        ctx_type_of_case = []
        if type_of_cases.count() > 0:

            for case_type in type_of_cases:
                ctx_type_of_case.append(case_type.case_type)
        if request.is_ajax():
            status = 200
            res = {
                'result': 'ok',
                'case_types': ctx_type_of_case,
            }
            response = simplejson.dumps(res)

            return HttpResponse(response, status=status, mimetype='application/json')

class AddTypeOfCase(View):

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            type_of_case, created = TypeOfCase.objects.get_or_create(case_type=request.POST['case_type'])
            status = 200
            res = {
                'result': 'ok',
                'case_name': type_of_case.case_type,
            }
            response = simplejson.dumps(res)

            return HttpResponse(response, status=status, mimetype='application/json')



