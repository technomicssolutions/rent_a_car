import simplejson
import ast
from datetime import datetime

from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.db.models import Max
from django.utils import timezone

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

class AddClient(View):

    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, 'add_client.html', context)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            client_details = ast.literal_eval(request.POST['client_details'])
            status = 200
            try:
                try:
                    client = Client.objects.get(phone_number=client_details['home_ph_no'])
                    message = 'Client with this Phone No is already existing'
                except Exception as ex:
                    client = Client.objects.get(passport_no=client_details['passport_no'])
                    message = 'Client with this Passport No is already existing'
                res = {
                    'result': 'error',
                    'message': message,
                }
            except Exception as ex:

                client = Client.objects.create(phone_number=client_details['home_ph_no'], passport_no=client_details['passport_no'])
                ctx_client = []
                client.name = client_details['name']
                client.address = request.POST['client_home_address']
                client.nationality = client_details['nationality']
                client.dob = datetime.strptime(client_details['dob'], '%d/%m/%Y')
                client.phone_number = client_details['home_ph_no']
                client.work_address = request.POST['client_work_address']
                client.work_ph_no = client_details['work_ph_no']

                client.license_no = client_details['license_no']
                client.license_type = client_details['license_type']
                client.date_of_issue = datetime.strptime(client_details['date_of_license_issue'], '%d/%m/%Y')
                client.issued_by = client_details['issued_by']
                client.expiry_license_date = datetime.strptime(client_details['expiry_date'], '%d/%m/%Y')
                
                client.passport_no = client_details['passport_no']
                client.date_of_passport_issue = datetime.strptime(client_details['passport_issued_date'], '%d/%m/%Y')
                client.place_of_issue = client_details['place_of_issue']

                client.save()
                ctx_client.append({
                    'id': client.id,
                    'client_name': client.name,
                    'license_no': client.license_no,
                    'license_issue_date': client.date_of_issue.strftime('%d/%m/%Y'),
                    'license_type': client.license_type,
                    'expiry_date': client.expiry_license_date.strftime('%d/%m/%Y'),
                    'passport_no': client.passport_no,
                    'passport_date_of_issue': client.date_of_passport_issue.strftime('%d/%m/%Y'),
                })
                res = {
                    'result': 'ok',
                    'client_data': ctx_client,
                }

            response = simplejson.dumps(res)

            return HttpResponse(response, status=status, mimetype='application/json')

class ClientList(View):

    def get(self, request, *args, **kwargs):

        clients = Client.objects.all().order_by('id')
        ctx_clients = []
        if request.is_ajax():
            if clients.count() > 0:
                for client in clients:
                    ctx_clients.append({
                        'id': client.id if client else '',
                        'client_name': client.name if client else '',
                        'license_no': client.license_no if client else '',
                        'license_issue_date': client.date_of_issue.strftime('%d/%m/%Y') if client.date_of_issue else '',
                        'license_type': client.license_type if client else '',
                        'expiry_date': client.expiry_license_date.strftime('%d/%m/%Y') if client.expiry_license_date else '',
                        'passport_no': client.passport_no if client else '',
                        'passport_date_of_issue': client.date_of_passport_issue.strftime('%d/%m/%Y') if client.date_of_passport_issue else '',


                    })
            res = {
                'clients': ctx_clients,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')

        context = {
            'clients': clients,
        }
        return render(request, 'clients.html', context)

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
        if request.is_ajax():
            vehicles = Vehicle.objects.filter(is_available=True).order_by('id')
            if vehicles.count() > 0:
                for vehicle in vehicles:
                    ctx_vehicles.append({
                        'id': vehicle.id,
                        'vehicle_no': vehicle.vehicle_no,
                        'plate_no': vehicle.plate_no,
                        'vehicle_type': vehicle.vehicle_type_name.vehicle_type_name,
                        'meter_reading': vehicle.meter_reading,
                        'vehicle_condition': vehicle.vehicle_condition,
                        'color': vehicle.vehicle_color,
                        'insuranse_value': vehicle.insuranse_value,
                        'type_of_insuranse': vehicle.type_of_insuranse,
                    })
            res = {
                'vehicles': ctx_vehicles
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
                vehicle.save()
                res = {
                    'result': 'ok'
                }
                
            except Exception as ex:
                print "Exception == ", str(ex)
                
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class EditClient(View):

    def get(self, request, *args, **kwargs):

        client_id = kwargs['client_id']
        ctx_client = []
        client = Client.objects.get(id=int(client_id))
        if request.is_ajax():
            ctx_client.append({
                'name': client.name ,
                'nationality': client.nationality ,
                'dob': client.dob.strftime('%d/%m/%Y') ,
                'home_ph_no': client.phone_number ,
                'work_ph_no': client.work_ph_no ,
                'license_no': client.license_no ,
                'license_type': client.license_type ,
                'date_of_license_issue': client.date_of_issue.strftime('%d/%m/%Y') ,
                'issued_by': client.issued_by ,
                'expiry_date': client.expiry_license_date.strftime('%d/%m/%Y') ,
                'passport_no': client.passport_no ,
                'passport_issued_date': client.date_of_passport_issue.strftime('%d/%m/%Y') ,
                'place_of_issue': client.place_of_issue ,
                'home_address': client.address ,
                'work_address': client.work_address ,
            })
            res = {
                'client': ctx_client,
            }
            status = 200
            response = simplejson.dumps(res)

            return HttpResponse(response, status=status, mimetype='application/json')
        context = {
            'client_id': client.id,
        }

        return render(request, 'edit_client.html', context)
    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            client_id = kwargs['client_id']
            status = 200
            client_details = ast.literal_eval(request.POST['client_details'])
            try:
                client = Client.objects.get(id=int(client_id))                
                # try:
                clients = Client.objects.filter(phone_number =client_details['home_ph_no']).exclude(id=client_id).count()
                if clients:
                    res = {
                        'result': 'error',
                        'message': 'Client with this phone number exists',
                    }
                    response = simplejson.dumps(res)
                    return HttpResponse(response, status=status, mimetype='application/json')
                else:
                    client.phone_number = client_details['home_ph_no']
                # except:
                #     client.phone_number = client_details['home_ph_no']
                client.passport_no = client_details['passport_no']
                client.name = client_details['name']
                client.address = request.POST['client_home_address']
                client.nationality = client_details['nationality']
                client.dob = datetime.strptime(client_details['dob'], '%d/%m/%Y')
                client.phone_number = client_details['home_ph_no']
                client.work_address = request.POST['client_work_address']
                client.work_ph_no = client_details['work_ph_no']

                client.license_no = client_details['license_no']
                client.license_type = client_details['license_type']
                client.date_of_issue = datetime.strptime(client_details['date_of_license_issue'], '%d/%m/%Y')
                client.issued_by = client_details['issued_by']
                client.expiry_license_date = datetime.strptime(client_details['expiry_date'], '%d/%m/%Y')
                
                # try:
                clients = Client.objects.filter(passport_no = client_details['passport_no']).exclude(id=client_id).count()
                if clients:
                    res = {
                        'result': 'error',
                        'message': 'Client with this passport number exists',
                    }
                    response = simplejson.dumps(res)
                    return HttpResponse(response, status=status, mimetype='application/json')
                else:
                    client.passport_no = client_details['passport_no']
                # except:
                #     client.passport_no = client_details['passport_no']
                client.date_of_passport_issue = datetime.strptime(client_details['passport_issued_date'], '%d/%m/%Y')
                client.place_of_issue = client_details['place_of_issue']

                client.save()
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
            try:
                rent_agreement, agreement_created = RentAgreement.objects.get_or_create(agreement_no=rent_agreement_details['agreement_no'])
                # if agreement_created:
                client = Client.objects.get(id=int(rent_agreement_details['client_id']))
                vehicle = Vehicle.objects.get(id=int(rent_agreement_details['vehicle_id']))
                rent_agreement.client = client
                rent_agreement.vehicle = vehicle
                rent_agreement.agreement_type = rent_agreement_details['agreement_type']
                rent_agreement.agreement_date = datetime.strptime(rent_agreement_details['date'], '%d/%m/%Y')
                rent_agreement.starting_date_time = datetime.strptime(rent_agreement_details['start_date_time'], '%d/%m/%Y %H:%M')
                rent_agreement.end_date_time = datetime.strptime(rent_agreement_details['end_date_time'], '%d/%m/%Y %H:%M') 
                rent_agreement.rent_type = rent_agreement_details['rent_type']
                rent_agreement.type_of_contract = rent_agreement_details['type_of_contract']
                if rent_agreement_details['with_driver'] == 'yes':
                    rent_agreement.with_driver = True
                else:
                    rent_agreement.with_driver = False
                if rent_agreement_details['with_driver'] == 'yes':
                    driver = Driver.objects.get(id=int(rent_agreement_details['driver_id']))
                    driver.is_available = False
                    driver.save()
                    rent_agreement.driver = driver
                rent_agreement.notes = rent_agreement_details['notes']
                rent_agreement.total_amount = rent_agreement_details['amount']
                rent_agreement.commission = rent_agreement_details['commission']
                rent_agreement.reduction = rent_agreement_details['reduction']
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
            receive_car.fine = receive_car_details['fine']
            receive_car.extra_charge = receive_car_details['extra_charge']
            receive_car.accident_passable = receive_car_details['accident_passable']
            receive_car.credit_card_no = receive_car_details['credit_card_no']
            receive_car.cheque_no = receive_car_details['cheque_no']
            receive_car.expiry_date = receive_car_details['card_expiry_date']
            receive_car.total_amount = receive_car_details['total_amount']
            receive_car.paid = receive_car_details['paid']
            receive_car.notes = receive_car_details['notes']
            receive_car.new_meter_reading = receive_car_details['meter_reading']
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
            agreements = RentAgreement.objects.filter(is_completed=False, agreement_no__startswith=agreement_no, starting_date_time__lte=current_date)
        except Exception as ex:
            print "************************************"
            print str(ex)
        ctx_agreements = []
        if request.is_ajax():
            if agreements.count() > 0:
                for agreement in agreements:
                    ctx_agreements.append({
                        'id': agreement.id,
                        'agreement_no': agreement.agreement_no,
                        'agreement_type': agreement.agreement_type,
                        'client': agreement.client.name if agreement.client else '',
                        'vehicle_no': agreement.vehicle.vehicle_no if agreement.vehicle else '',
                        'rent': agreement.rent,
                        'date': agreement.agreement_date.strftime('%d/%m/%Y'),
                        'begining_date': agreement.starting_date_time.strftime('%d/%m/%Y'),
                        'begining_time': agreement.starting_date_time.strftime('%H:%M'),
                        'end_date': agreement.end_date_time.strftime('%d/%m/%Y'),
                        'end_time': agreement.end_date_time.strftime('%H:%M'),
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
                        'with_driver': 'yes' if agreement.with_driver else 'no',
                        'driver_name': agreement.driver.driver_name if agreement.driver else '',
                        'driver_passport_no': agreement.driver.driver_passport_no if agreement.driver else '',
                        'sponsar_name': agreement.driver.sponsar_name if agreement.driver else '',
                        'paid': agreement.paid,
                        'late_message': 'Late receival' if agreement.end_date_time < current_date else '',
                    })
                    
            res = {
                'result': 'ok',
                'agreements': ctx_agreements,
            }
            status = 200
            response = simplejson.dumps(res)

            return HttpResponse(response, status=status, mimetype='application/json')

class PrintRentAgreement(View):

    def get(self, request, *args, **kwargs):

        agreement_id = kwargs['agreement_id']
        rent_agreement = RentAgreement.objects.get(id=agreement_id)

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
        table.drawOn(p,50, 1180) 
        p.setFont("Helvetica", 16)
        p.drawString(50, 1120, 'Tel : 02-6266634')
        p.drawString(50, 1100, 'Mob : 055-4087528')
        p.drawString(50, 1080, 'P.O.Box : 32900')
        p.drawString(50, 1060, 'Old Passport Road')
        p.drawString(50, 1040, 'Abu Dhabi - UAE')
        
        p.drawString(50, 1010, 'Date : ......................')
        p.setFont("Helvetica", 13)
        p.drawString(90, 1015, rent_agreement.agreement_date.strftime('%d/%m/%Y'))
        p.setFont("Helvetica-Bold", 15)
        p.drawString(410, 1010, 'RENTAL AGREEMENT')
        p.line(50,1000,950,1000)
        p.line(500,1000,500,150)
        p.line(250,1000, 250, 900)
        p.line(50, 950, 950,950)
        p.line(50, 900, 950, 900)
        p.line(50, 850, 950, 850)
        p.line(375,900, 375, 850)
        p.line(50, 800, 950, 800)
        p.line(50, 750, 950, 750)
        p.line(50, 700, 950, 700)
        p.line(50, 650, 950, 650)
        p.line(50, 575, 950, 575)
        # p.line(50, 500, 950, 500)
        # p.line(50, 550, 950, 550)

        p.drawString(80, 980, 'Vehicle Type')
        p.drawString(280, 980, 'Reg. No.')
        p.drawString(80, 930, 'Vehicle Make')
        p.drawString(280, 930, 'Vehicle Color')
        p.drawString(170, 880, 'Leaving Date')
        p.drawString(400, 880, 'Time')
        p.drawString(170, 830, 'Meter Reading on Leaving')
        p.drawString(170, 780, 'Expecting Returning Date')

        p.setFont("Helvetica", 15)
        p.drawString(510, 970, 'Rental Name: ')
        p.drawString(510, 920, 'Nationality: ')
        p.drawString(510, 870, 'Date of Birth: ')
        p.drawString(510, 820, 'Passport No: ')
        p.drawString(510, 770, 'Date & Place of Issue: ')
        p.drawString(60, 720, 'License No: ')
        p.drawString(510, 720, 'Issued By: ')
        p.drawString(60, 670, 'Date Issued: ')
        p.drawString(510, 670, 'Expiry Date:')
        p.drawString(50, 620, 'Home Address:')
        p.drawString(510, 620, 'Tel No.:')
        p.drawString(60, 520, 'Total Amount:')



        p.setFont("Helvetica", 13)
        vehicle = rent_agreement.vehicle
        p.drawString(100, 960, vehicle.vehicle_type_name.vehicle_type_name if vehicle and vehicle.vehicle_type_name else '')
        p.drawString(300, 960, rent_agreement.agreement_no)
        p.drawString(100, 910, vehicle.vehicle_make if vehicle else '')
        p.drawString(300, 910, vehicle.vehicle_color if vehicle else '')
        p.drawString(200, 860, rent_agreement.starting_date_time.strftime('%d/%m/%Y'))
        p.drawString(400, 860, rent_agreement.starting_date_time.strftime('%H:%M'))
        p.drawString(200, 810, rent_agreement.vehicle.meter_reading)
        p.drawString(200, 760, rent_agreement.end_date_time.strftime('%d/%m/%Y'))

        p.drawString(610, 970, rent_agreement.client.name if rent_agreement.client else '')
        p.drawString(590, 920, rent_agreement.client.nationality if rent_agreement.client else '')
        p.drawString(600, 870, rent_agreement.client.dob.strftime('%d/%m/%Y') if rent_agreement.client else '')
        p.drawString(600, 820, rent_agreement.client.passport_no if rent_agreement.client else '')
        p.drawString(660, 770, (rent_agreement.client.date_of_passport_issue.strftime('%d/%m/%Y') if rent_agreement.client else '') + ' , ')
        p.drawString(739, 770, rent_agreement.client.place_of_issue if rent_agreement.client else '' )
        p.drawString(150, 720, rent_agreement.client.license_no if rent_agreement.client else '')
        p.drawString(600, 720, rent_agreement.client.issued_by if rent_agreement.client else '')
        p.drawString(150, 670, rent_agreement.client.date_of_issue.strftime('%d/%m/%Y') if rent_agreement.client else '')
        p.drawString(600, 670, rent_agreement.client.expiry_license_date.strftime('%d/%m/%Y') if rent_agreement.client else '')
        p.drawString(160, 620, rent_agreement.client.address if rent_agreement.client else '')
        p.drawString(600, 620, rent_agreement.client.phone_number if rent_agreement.client else '')
        p.drawString(160, 520, str(rent_agreement.rent))
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
                    'driver_license_issue_date': driver.driver_license_issue_date.strftime('%d/%m/%Y'),
                    'driver_license_issue_place': driver.driver_license_issue_place,
                    'driver_license_expiry_date': driver.driver_license_expiry_date.strftime('%d/%m/%Y'),
                    'driver_dob': driver.driver_dob.strftime('%d/%m/%Y'),
                    'sponsar_name': driver.sponsar_name,
                    'sponsar_address': driver.sponsar_address,
                    'sponsar_phone': driver.sponsar_phone,
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
