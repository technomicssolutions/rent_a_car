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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


from web.models import *

utc=pytz.UTC

font_path = settings.PROJECT_ROOT.replace("\\", "/")+"/header/fonts/KacstOne.ttf"
pdfmetrics.registerFont(TTFont('Arabic', font_path))

path = settings.PROJECT_ROOT.replace("\\", "/")+"/header/trophy.jpg"

def draw_arabic(x, y, text, canvas):

    p = canvas
    p.setFont('Arabic', 16)
    p.drawString(x, y, text)

    # x+= p.stringWidth(text)

    # p.drawString(x, y, text)

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
                    'petrol': vehicle.petrol,
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
                        'petrol': vehicle.petrol,
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
                        'petrol': vehicle.petrol,
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
            vehicle = Vehicle.objects.get(id=int(vehicle_id))
            vehicle_details = ast.literal_eval(request.POST['vehicle_details'])
            vehicle_type = VehicleType.objects.get(vehicle_type_name=vehicle_details['vehicle_type'])
            try:
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
                # except:
                #     vehicle.vehicle_no = vehicle_details['vehicle_no']
                # try:
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
                # except:
                #     vehicle.plate_no = vehicle_details['plate_no']
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
                
            except Exception as ex:
                print "Exception == ", str(ex)
                
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
            vehicle_details = ast.literal_eval(request.POST['vehicle_details'])
            try:
                rent_agreement, agreement_created = RentAgreement.objects.get_or_create(agreement_no=rent_agreement_details['agreement_no'])
                client = Client.objects.get(id=int(rent_agreement_details['client_id']))
                vehicle = Vehicle.objects.get(id=int(rent_agreement_details['vehicle_id']))
                rent_agreement.client = client
                rent_agreement.vehicle = vehicle
                if int(vehicle.meter_reading) != int(vehicle_details['meter_reading']):
                    vehicle.meter_reading = vehicle_details['meter_reading']
                    vehicle.save()
                rent_agreement.leaving_meterreading = vehicle_details['meter_reading']
                rent_agreement.leaving_petrol = vehicle.petrol
                rent_agreement.client_identity = rent_agreement_details['client_identity']
                rent_agreement.agreement_date = datetime.strptime(rent_agreement_details['date'], '%d/%m/%Y')
                start_date_time = utc.localize(datetime.strptime(rent_agreement_details['start_date_time'], '%d/%m/%Y %I:%M%p'))
                end_date_time = utc.localize(datetime.strptime(rent_agreement_details['end_date_time'], '%d/%m/%Y %I:%M%p' ))
                rent_agreement.starting_date_time = start_date_time
                rent_agreement.end_date_time = end_date_time
                rent_agreement.rent_type = rent_agreement_details['rent_type']
                rent_agreement.vehicle_scratch = rent_agreement_details['vehicle_scratch']
                rent_agreement.accident_passable = rent_agreement_details['accident_passable']
                driver = Driver.objects.get(id=int(rent_agreement_details['driver_id']))
                driver.is_available = False
                driver.save()
                rent_agreement.driver = driver
                rent_agreement.notes = rent_agreement_details['notes']
                rent_agreement.total_amount = rent_agreement_details['amount']
                rent_agreement.rent = rent_agreement_details['rent']
                rent_agreement.paid = rent_agreement_details['paid']
                rent_agreement.save()
                client.rent = float(client.rent) + float(rent_agreement_details['rent'])
                client.paid = float(client.paid) + float(rent_agreement_details['paid'])
                client.balance = float(client.rent) - float(client.paid)
                client.save()
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
            receive_car.vehicle_scratch = receive_car_details['vehicle_scratch']
            receive_car.fine = receive_car_details['fine']
            receive_car.extra_charge = receive_car_details['extra_charge']
            receive_car.accident_passable = receive_car_details['accident_passable']
            receive_car.credit_card_no = receive_car_details['credit_card_no']
            receive_car.cheque_no = receive_car_details['cheque_no']
            receive_car.total_amount = receive_car_details['total_amount']
            receive_car.paid = receive_car_details['paid']
            receive_car.reduction = receive_car_details['reduction']
            receive_car.notes = receive_car_details['notes']
            receive_car.new_meter_reading = receive_car_details['meter_reading']
            receive_car.leaving_petrol = receive_car_details['returning_petrol']
            receive_car.vehicle_scratch = receive_car_details['vehicle_scratch']
            receive_car.receipt_datetime = utc.localize(datetime.strptime(receive_car_details['receipt_date'], '%d/%m/%Y %I:%M%p'))

            receive_car.returning_date_time = utc.localize(datetime.strptime(receive_car_details['returning_date'], '%d/%m/%Y %I:%M%p'))
            receive_car.save()
            client = rent_agreement.client
            client.rent = float(client.rent) - float(rent_agreement.rent)
            client.rent = float(client.rent) + float(receive_car.total_amount)
            client.paid = float(client.paid) + float(receive_car.paid)
            client.balance = float(client.rent) - float(client.paid)
            client.save() 
            vehicle = rent_agreement.vehicle
            vehicle.meter_reading = receive_car.new_meter_reading
            if receive_car_details['balance'] == 0:
                vehicle.is_available = True
                rent_agreement.is_completed = True
                rent_agreement.save()
                driver = rent_agreement.driver
                driver.is_available = True
                driver.save()
                
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
                        'client': agreement.client.name if agreement.client else '',
                        'vehicle_no': agreement.vehicle.vehicle_no if agreement.vehicle else '',
                        'rent': agreement.rent,
                        'date': agreement.agreement_date.strftime('%d/%m/%Y') if agreement.agreement_date else '',
                        'begining_date': agreement.starting_date_time.strftime('%d/%m/%Y') if agreement.starting_date_time else '',
                        'begining_time': agreement.starting_date_time.strftime('%I:%M%p') if agreement.starting_date_time else '',
                        'end_date': agreement.end_date_time.strftime('%d/%m/%Y') if agreement.end_date_time else '',
                        'end_time': agreement.end_date_time.strftime('%I:%M%p') if agreement.end_date_time else '',
                        'license_no': agreement.client.license_no if agreement.client else '',
                        'license_type': agreement.client.license_type if agreement.client else '',
                        'license_date': agreement.client.date_of_issue.strftime('%d/%m/%Y') if agreement.client else '',
                        'passport_no': agreement.client.passport_no if agreement.client else '',
                        'place_of_issue': agreement.client.place_of_issue if agreement.client else '', 
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
                        'vehicle_scratch': agreement.vehicle_scratch if agreement.vehicle_scratch else '',
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
                    'client': agreement.client.name if agreement.client else '',
                    'vehicle_no': agreement.vehicle.vehicle_no if agreement.vehicle else '',
                    'rent': agreement.rent,
                    'date': agreement.agreement_date.strftime('%d/%m/%Y'),
                    'begining_date': agreement.starting_date_time.strftime('%d/%m/%Y'),
                    'begining_time': agreement.starting_date_time.strftime('%I:%M%p'),
                    'end_date': agreement.end_date_time.strftime('%d/%m/%Y'),
                    'end_time': agreement.end_date_time.strftime('%I:%M%p'),
                    'license_no': agreement.client.license_no if agreement.client else '',
                    'license_type': agreement.client.license_type if agreement.client else '',
                    'license_date': agreement.client.date_of_issue.strftime('%d/%m/%Y') if agreement.client else '',
                    'passport_no': agreement.client.passport_no if agreement.client else '',
                    'place_of_issue': agreement.client.place_of_issue if agreement.client else '', 
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
                    'vehicle_scratch': agreement.vehicle_scratch if agreement.vehicle_scratch else '',
                    'late_message': 'Late receival' if agreement.end_date_time < current_date else '',
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
                    'client': agreement.client.name if agreement.client else '',
                    'vehicle_no': agreement.vehicle.vehicle_no if agreement.vehicle else '',
                    'rent': agreement.rent,
                    'date': agreement.agreement_date.strftime('%d/%m/%Y') if agreement.agreement_date else '',
                    'begining_date': agreement.starting_date_time.strftime('%d/%m/%Y') if agreement.starting_date_time else '',
                    'begining_time': agreement.starting_date_time.strftime('%I:%M%p ') if agreement.starting_date_time else '',
                    'end_date': agreement.end_date_time.strftime('%d/%m/%Y') if agreement.end_date_time else '',
                    'end_time': agreement.end_date_time.strftime('%I:%M%p ') if agreement.end_date_time else '',
                    'license_no': agreement.client.license_no if agreement.client else '',
                    'license_type': agreement.client.license_type if agreement.client else '',
                    'license_date': agreement.client.date_of_issue.strftime('%d/%m/%Y') if agreement.client else '',
                    'passport_no': agreement.client.passport_no if agreement.client else '',
                    'place_of_issue': agreement.client.place_of_issue if agreement.client else '', 
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
                    'damage': agreement.accident_passable if agreement.accident_passable else '',
                    'vehicle_scratch': agreement.vehicle_scratch if agreement.vehicle_scratch else '',
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
            style = [
                ('FONTSIZE', (0,0), (-1, -1), 20),
                ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
            ]

            new_style = [
                ('FONTSIZE', (0,0), (-1, -1), 30),
                ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
            ]

            para_style = ParagraphStyle('fancy')
            para_style.fontSize = 35
            para_style.fontName = 'Helvetica-Bold'
            para = Paragraph('Golden Cup Rent A Car', para_style)

            data =[[ para , '']]
            
            table = Table(data, colWidths=[500, 100], rowHeights=50, style=style)
            table.wrapOn(p, 200, 400)
            table.drawOn(p, 300, 1180)

            p.drawImage(path, 70, 1065, width=30*cm, height=3*cm, preserveAspectRatio=True)

            p.setFont("Helvetica", 12)
            p.drawString(350, 1050, 'Tel : 02-6266634 , Mob : 055-4087528 , P.O.Box : 32900')
            
            p.drawString(400, 1036, 'Old Passport Road , Abu Dhabi - UAE')
            p.setFont("Helvetica", 16)
            p.drawString(50, 1010, 'Date : ......................')
            p.setFont("Helvetica", 13)
            p.drawString(90, 1015, rent_agreement.agreement_date.strftime('%d/%m/%Y'))
            p.setFont("Helvetica-Bold", 15)
            p.drawString(410, 1010, 'RENTAL AGREEMENT')
            p.line(50, 1000, 950, 1000)
            p.line(500, 1000, 500, 150)
            p.line(250, 1000, 250, 900)
            p.line(50, 950, 950, 950)
            p.line(50, 900, 950, 900)
            p.line(50, 850, 950, 850)
            p.line(375,900, 375, 850)
            p.line(50, 800, 950, 800)
            p.line(375, 800, 375, 750)
            p.line(50, 750, 950, 750)
            p.line(50, 700, 950, 700)
            p.line(50, 650, 950, 650)
            p.line(50, 600, 950, 600)
            p.line(250, 600, 250, 750)
            p.line(750, 650, 750, 750)
            p.line(750, 900, 750, 1000)
            p.line(750, 800, 750, 850)

            p.line(250, 400, 250, 750)
            p.line(300, 850, 300, 800)
            p.line(50, 500, 500, 500)
            p.line(50, 550, 500, 550)
            p.line(50, 450, 500, 450)
            p.line(50, 400, 500, 400)
            p.line(500, 550, 950, 550)
            p.line(500, 500, 950, 500)

            p.drawString(80, 980, 'Vehicle Type')
            p.drawString(280, 980, 'Reg. No.')
            p.drawString(80, 930, 'Vehicle Make')
            p.drawString(280, 930, 'Vehicle Color')
            p.drawString(170, 880, 'Leaving Date')
            p.drawString(400, 880, 'Time')
            p.drawString(60, 830, 'Meter Reading on Leaving')
            p.drawString(310, 830, 'Petrol on Leaving')
            p.drawString(170, 780, 'Expecting Returning Date')
            p.drawString(400, 780, 'Time')

            p.setFont("Helvetica", 15)
            p.drawString(510, 970, 'Rental Name: ')
            p.drawString(760, 970, 'Nationality: ')
            p.drawString(510, 920, 'Date of Birth: ')
            p.drawString(760, 920, 'Passport No: ')
            p.drawString(510, 770, 'Date & Place of Issue: ')
            p.drawString(560,730, 'License No: ')
            p.drawString(770,730, 'Issued By: ')
            p.drawString(560, 680, 'Date Issued: ')
            p.drawString(770, 680, 'Expiry Date:')
            p.drawString(510, 880, 'Home Address:')
            p.drawString(510, 830, 'Tel No.:')
            p.drawString(760, 830, 'Client Identity:')

            p.drawString(100, 570, 'Amount')
            p.drawString(100, 520, 'Total Amount')
            p.drawString(100, 470, 'Paid')
            p.drawString(100, 420, 'Balance')

            p.drawString(100, 730, 'Driver Name')
            p.drawString(300, 730, 'License No')
            p.drawString(100, 680, 'Passport No')
            p.drawString(300, 680, 'Nationality')

            p.drawString(100, 630, 'Sponsar Name')
            p.drawString(300, 630, 'Sponsar Tel.')
            p.drawString(610, 630, 'Sponsar Address')
            p.drawString(610, 580, 'Driver Working Address')
            p.drawString(610, 530, 'Driver Tel. No')


            p.setFont("Helvetica", 13)
            vehicle = rent_agreement.vehicle
            p.drawString(100, 960, vehicle.vehicle_type_name.vehicle_type_name if vehicle and vehicle.vehicle_type_name else '')
            p.drawString(300, 960, rent_agreement.agreement_no)
            p.drawString(100, 910, vehicle.vehicle_make if vehicle else '')
            p.drawString(300, 910, vehicle.vehicle_color if vehicle else '')
            p.drawString(200, 860, rent_agreement.starting_date_time.strftime('%d/%m/%Y'))
            p.drawString(400, 860, rent_agreement.starting_date_time.strftime('%I:%M %p'))
            p.drawString(150, 810, rent_agreement.leaving_meterreading if rent_agreement.leaving_meterreading else '')
            p.drawString(380, 810, rent_agreement.leaving_petrol)
            p.drawString(200, 760, rent_agreement.end_date_time.strftime('%d/%m/%Y'))
            p.drawString(400, 760, rent_agreement.end_date_time.strftime('%I:%M %p'))

            p.drawString(610, 970, rent_agreement.client.name if rent_agreement.client else '')
            p.drawString(840, 970, rent_agreement.client.nationality if rent_agreement.client else '')
            p.drawString(600, 920, rent_agreement.client.dob.strftime('%d/%m/%Y') if rent_agreement.client else '')
            p.drawString(850, 920, rent_agreement.client.passport_no if rent_agreement.client else '')
            p.drawString(660, 770, (rent_agreement.client.date_of_passport_issue.strftime('%d/%m/%Y') if rent_agreement.client else '') + ' , ')
            p.drawString(739, 770, rent_agreement.client.place_of_issue if rent_agreement.client else '' )
            p.drawString(580, 710, rent_agreement.client.license_no if rent_agreement.client else '')
            p.drawString(790, 710, rent_agreement.client.issued_by if rent_agreement.client else '')
            p.drawString(580, 660, rent_agreement.client.date_of_issue.strftime('%d/%m/%Y') if rent_agreement.client else '')
            p.drawString(790, 660, rent_agreement.client.expiry_license_date.strftime('%d/%m/%Y') if rent_agreement.client else '')
            p.drawString(620, 880, rent_agreement.client.address if rent_agreement.client else '')
            p.drawString(600, 830, rent_agreement.client.phone_number if rent_agreement.client else '')
            p.drawString(860, 830, rent_agreement.client_identity if rent_agreement.client_identity else 'Driving License')
            

            p.drawString(130, 710, rent_agreement.driver.driver_name)
            p.drawString(320, 710, rent_agreement.driver.driver_nationality)
            p.drawString(130, 660, rent_agreement.driver.driver_passport_no)
            p.drawString(320, 660, rent_agreement.driver.driver_nationality)

            p.drawString(140, 610, rent_agreement.driver.sponsar_name)
            p.drawString(340, 610, rent_agreement.driver.sponsar_phone)
            p.drawString(550, 610, rent_agreement.driver.sponsar_address)

            p.drawString(260, 570, str(rent_agreement.rent))
            p.drawString(260, 520, str(rent_agreement.total_amount))
            p.drawString(260, 470, str(rent_agreement.paid))
            p.drawString(260, 420, str(float(rent_agreement.total_amount) - float(rent_agreement.paid)))
            p.drawString(610, 560, str(rent_agreement.driver.driver_working_address))
            p.drawString(610, 510, str(rent_agreement.driver.driver_working_ph))

            p.drawString(60, 200, """This vehicle cann't be taken outside the UAE without prior permission""")
            p.drawString(60, 180, """ of the owner in writing""")
            p.drawString(503, 400, """I the undersigned agree to rent from the owner the above mentioned vehcile""")
            p.drawString(503, 380, """for the period set our herein. I have read the terms and conditions det out on""")
            p.drawString(503, 360, """the reverse of this agreement between my self and the owner. I certify that """)
            p.drawString(503, 340, """the particualrs which i have given are true""")
            # p.drawString()
            p.drawString(503, 280, """ In the Event of any Accident The Renter is Liable to pay Hire.""")
            p.drawString(503, 180,'SIGNATURE :.........................................................................')
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
                    driver = Driver.objects.get(driver_passport_no=driver_details['passport_no'])
                    message = 'Driver with this Passport No is already existing'
                res = {
                    'result': 'error',
                    'message': message,
                }
            except Exception as ex:
                print str(ex)
                driver = Driver.objects.create(driver_phone=driver_details['home_ph_no'], driver_passport_no=driver_details['passport_no'])
                driver.driver_name = driver_details['name']  

                driver.driver_address = request.POST['home_address'] 
                driver.driver_nationality = driver_details['nationality']
                driver.driver_license_no = driver_details['license_no']
                driver.driver_license_issue_date = datetime.strptime(driver_details['date_of_license_issue'], '%d/%m/%Y')
                driver.driver_license_issue_place = driver_details['issued_place']
                driver.driver_license_expiry_date = datetime.strptime(driver_details['expiry_date'], '%d/%m/%Y')
                driver.driver_dob = datetime.strptime(driver_details['dob'], '%d/%m/%Y')
                driver.sponsar_name = driver_details['sponsar_name']
                driver.sponsar_address = request.POST['sponsar_address']
                driver.sponsar_phone = driver_details['sponsar_ph']
                driver.driver_working_address = request.POST['driver_working_address']
                driver.driver_working_ph = driver_details['working_tel_no']
                driver.save()
                ctx_driver.append({
                    'id': driver.id,
                    'driver_name': driver.driver_name,
                    'driver_address': driver.driver_address,
                    'driver_phone': driver.driver_phone,
                    'driver_nationality': driver.driver_nationality,
                    'driver_license_no': driver.driver_license_no,
                    'driver_license_issue_date': driver.driver_license_issue_date.strftime('%d/%m/%Y'),
                    'driver_license_issue_place': driver.driver_license_issue_place,
                    'driver_license_expiry_date': driver.driver_license_expiry_date.strftime('%d/%m/%Y'),
                    'driver_dob': driver.driver_dob.strftime('%d/%m/%Y'),
                    'sponsar_name': driver.sponsar_name,
                    'sponsar_address': driver.sponsar_address,
                    'sponsar_phone': driver.sponsar_phone,
                    'passport_no': driver.driver_passport_no,
                    'driver_working_address': driver.driver_working_address,
                    'working_tel_no': driver.driver_working_ph
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
            drivers = Driver.objects.filter(is_available=True).order_by('id')
            for driver in drivers:
                ctx_drivers.append({
                    'id': driver.id,
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
                    'working_tel_no': driver.driver_working_ph
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
            style = [
                ('FONTSIZE', (0,0), (-1, -1), 20),
                ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
            ]

            new_style = [
                ('FONTSIZE', (0,0), (-1, -1), 30),
                ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
            ]

            para_style = ParagraphStyle('fancy')
            para_style.fontSize = 35
            para_style.fontName = 'Helvetica-Bold'
            para = Paragraph('Golden Cup Rent A Car', para_style)

            data =[[ para , '']]
            
            table = Table(data, colWidths=[500, 100], rowHeights=50, style=style)
            table.wrapOn(p, 200, 400)
            table.drawOn(p, 300, 1180) 

            p.drawImage(path, 70, 1065, width=30*cm, height=3*cm, preserveAspectRatio=True)

            p.setFont("Helvetica", 12)
            p.drawString(350, 1050, 'Tel : 02-6266634 , Mob : 055-4087528 , P.O.Box : 32900')
            
            p.drawString(400, 1036, 'Old Passport Road , Abu Dhabi - UAE')
            p.setFont("Helvetica", 16)
            p.drawString(50, 1010, 'Date : ......................')
            p.setFont("Helvetica", 13)
            p.drawString(100, 1015,receive_car.receipt_datetime.strftime('%d/%m/%Y') if receive_car.receipt_datetime else '')
            p.setFont("Helvetica-Bold", 15)
            p.drawString(410, 1010, 'RENTAL CAR RECEIPT')
            p.line(50,1000,950,1000)
            p.line(500,1000,500,100)
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
            p.line(50, 450, 950, 450)
            p.line(500, 410, 950, 410)
            p.line(500, 370, 950, 370)
            p.line(500, 330, 950, 330)
            p.line(500, 290, 950, 290)
            p.line(500, 250, 950, 250)
            p.line(500, 210, 950, 210)
            p.line(500, 170, 950, 170)
            p.line(500, 130, 950, 130)
            p.line(500, 100, 950, 100)
            p.line(500, 70, 950, 70)
            p.line(250, 550, 250, 500)
            p.line(250, 500, 250, 450)
            p.line(750, 500, 750, 550)
            
            p.line(750, 450, 750, 100)
            p.line(500, 70, 500, 100)
            p.line(750, 70, 750, 100)

            p.setFont("Helvetica", 15)
            p.drawString(50, 980, 'Driver Name: ')
            p.drawString(50, 930, 'Nationality: ')
            p.drawString(50, 880, 'Passport No: ')
            p.drawString(50, 830, 'Address:')
            p.drawString(50, 780, 'D.License No: ')
            p.drawString(50, 730, 'License Issue Date - Expiry Date : ')

            p.drawString(510, 970, 'Name: ')
            p.drawString(510, 920, 'Nationality: ')
            p.drawString(510, 870, 'Date of Birth: ')
            p.drawString(510, 820, 'Passport No: ')
            p.drawString(510, 770, 'Date & Place of Issue: ')
            
            p.drawString(510, 720, 'License Issued By: ')
            p.drawString(50, 670, 'Leaving Date: ')
            p.drawString(260, 670, 'Time: ')
            p.drawString(510, 670, 'License Expiry Date:')
            p.drawString(50, 620, 'Returning Date:')
            p.drawString(260, 620, 'Time: ' )
            p.drawString(510, 620, 'Tel No.:')
            p.drawString(510, 580, 'Address: ')
            p.drawString(50, 580, 'Entering Date:')
            p.drawString(260, 580, 'Time: ' )

            p.drawString(50, 530, 'Plate No: ')
            p.drawString(260, 530, 'Car Color: ')
            p.drawString(50, 480, 'Model: ')
            p.drawString(260, 480, 'Made: ')
            p.drawString(510, 530, 'Return Meter Reading: ')
            p.drawString(760, 530, 'Petrol on Returning ')
            p.drawString(510, 480, 'Insurance Value: ')

            p.drawString(760, 430, 'Deposit')
            p.drawString(760, 380, 'Fine')
            p.drawString(760, 340, 'Petrol')
            p.drawString(760, 310, 'Accident Passable')
            p.drawString(760, 270, 'Vehicle Scrtach')
            p.drawString(760, 230, 'Extra Charge')
            p.drawString(760, 190, 'Reduction')
            p.drawString(760, 150, 'Rent')
            p.drawString(760, 110, 'Total Amount')
            p.drawString(760, 80, 'Balance')

            p.drawString(60, 420, "We don't receipt the car in Thursday, Friday the formal holiday")
            p.drawString(60, 380, "Acknowledge that I have read the above and reverse method")
            p.drawString(60, 340, "terms and conditions and agree to able by them")
            p.drawString(100, 300, '................................. Sponsor')
            p.drawString(350, 300, '....................... Hirer')
            p.drawString(250, 120, '..............................Office incharge')

            p.drawString(150, 980, receive_car.rent_agreement.driver.driver_name)
            p.drawString(140, 930, receive_car.rent_agreement.driver.driver_nationality)
            p.drawString(140, 880, receive_car.rent_agreement.driver.driver_passport_no)
            p.drawString(120, 830, receive_car.rent_agreement.driver.driver_address.replace('\n', ' '))
            
            p.drawString(150, 780, receive_car.rent_agreement.driver.driver_license_no)
            p.drawString(280, 730, receive_car.rent_agreement.driver.driver_license_issue_date.strftime('%d/%m/%Y') + ' - ' + receive_car.rent_agreement.driver.driver_license_expiry_date.strftime('%d/%m/%Y'))

            p.drawString(560, 970, receive_car.rent_agreement.client.name)
            p.drawString(610, 920, receive_car.rent_agreement.client.nationality)
            p.drawString(610, 870, receive_car.rent_agreement.client.dob.strftime('%d/%m/%Y'))
            p.drawString(610, 820, receive_car.rent_agreement.client.passport_no)
            p.drawString(670, 770, receive_car.rent_agreement.client.date_of_passport_issue.strftime('%d/%m/%Y') + ' - '+receive_car.rent_agreement.client.place_of_issue)
            p.drawString(650, 720, receive_car.rent_agreement.client.issued_by)
            p.drawString(650, 670, receive_car.rent_agreement.client.expiry_license_date.strftime('%d/%m/%Y'))
            p.drawString(150, 670, receive_car.rent_agreement.starting_date_time.strftime('%d/%m/%Y'))
            p.drawString(300, 670, receive_car.rent_agreement.starting_date_time.strftime('%H:%M%p'))
            p.drawString(160, 620, receive_car.rent_agreement.end_date_time.strftime('%d/%m/%Y'))
            p.drawString(300, 620, receive_car.rent_agreement.end_date_time.strftime('%H:%M%p'))
            p.drawString(590, 620, receive_car.rent_agreement.client.phone_number)
            p.drawString(150, 580, receive_car.receipt_datetime.strftime('%d/%m/%Y') if receive_car.receipt_datetime else '')
            p.drawString(300, 580, receive_car.receipt_datetime.strftime('%H:%M%p') if receive_car.receipt_datetime else '')
            p.drawString(580, 580, receive_car.rent_agreement.client.address.replace('\n', ' '))
            p.drawString(140, 530, receive_car.rent_agreement.vehicle.plate_no)
            p.drawString(340, 530, receive_car.rent_agreement.vehicle.vehicle_color)
            p.drawString(110, 480, receive_car.rent_agreement.vehicle.vehicle_type_name.vehicle_type_name)
            p.drawString(330, 480, receive_car.rent_agreement.vehicle.vehicle_make)
            p.drawString(560, 510, str(receive_car.new_meter_reading))
            p.drawString(760, 510, receive_car.returning_petrol)
            p.drawString(650, 480, str(receive_car.rent_agreement.vehicle.insuranse_value))

            p.drawString(550, 430, str(receive_car.rent_agreement.paid))
            p.drawString(550, 380, str(receive_car.fine))
            p.drawString(550, 340, str(receive_car.petrol))
            p.drawString(550, 310, str(receive_car.accident_passable))
            p.drawString(550, 270, str(receive_car.vehicle_scratch))
            p.drawString(550, 230, str(receive_car.extra_charge))
            
            p.drawString(550, 190, str(receive_car.reduction))
            p.drawString(550, 150, str(receive_car.rent_agreement.rent))
            p.drawString(550, 110, str(receive_car.total_amount))
            p.drawString(550, 80, str(float(receive_car.total_amount) - (float(receive_car.paid) + float(receive_car.rent_agreement.paid))))

            p.showPage()
            p.save()

            return response

class CaseEntry(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'case_entry.html', {})

    def post(self, request, *args, **kwargs):

        if request.is_ajax():

            case_details = ast.literal_eval(request.POST['case_details'])
            client = Client.objects.get(id = int(case_details['client_id']))
            vehicle = Vehicle.objects.get(id=case_details['vehicle_id'])
            case = CaseDetail.objects.create(vehicle=vehicle, client=client)
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
        end_date = request.GET.get('end_date', '')
        vehicle_no = request.GET.get('vehicle_no', '')
        rent_agreements = []
        
        if start_date and end_date and vehicle_no:
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
            start_date = datetime.combine(start_date, dt.time.max)
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
            end_date = datetime.combine(end_date, dt.time.min)
            # rent_agreements = RentAgreement.objects.filter(vehicle__vehicle_no=vehicle_no)
            # rent_agreements = RentAgreement.objects.filter(vehicle__vehicle_no__contains=vehicle_no, starting_date_time__range=(
            #             datetime.combine(start_date, dt.time.min),
            #             datetime.combine(start_date, dt.time.max)), end_date_time__range=(
            #             datetime.combine(end_date, dt.time.min),
            #             datetime.combine(end_date, dt.time.max)
            #             ))
            rent_agreements = RentAgreement.objects.filter(Q(vehicle__vehicle_no__icontains=vehicle_no),Q(starting_date_time__lte=start_date, end_date_time__gte=end_date))
            
        if request.is_ajax():
            res = {
                'result': 'ok',
                'client_name': rent_agreements[0].client.name if rent_agreements else '',
                'client_id': rent_agreements[0].client.id if rent_agreements else '',
                'vehicle_id': rent_agreements[0].vehicle.id if rent_agreements else '',
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



