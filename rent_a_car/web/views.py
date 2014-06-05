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
            print client_details
            client, created = Client.objects.get_or_create(phone_number=client_details['home_ph_no'], passport_no=client_details['passport_no'])
            if created:
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
                res = {
                    'result': 'ok',
                }
                status = 200
            else:
                res = {
                    'result': 'error',
                    'message': 'Customer with this passport no, Tel No.(Home) is already existing'
                }
                status = 500

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

        if request.is_ajax():
            vehicle_details = ast.literal_eval(request.POST['vehicle_details'])
            try:
                vehicle = Vehicle.objects.get(vehicle_no=vehicle_details['vehicle_no'],plate_no=vehicle_details['plate_no'])
                res = {
                    'result': 'error',
                    'message': 'Vehicle with this Vehicle No. and Plate No. is already existing'
                }
                status = 500
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
                vehicle.save()
                res = {
                    'result': 'ok',
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

            vehicle_id = kwargs['vehicle_id']
            vehicle = Vehicle.objects.get(id=int(vehicle_id))
            vehicle_details = ast.literal_eval(request.POST['vehicle_details'])
            vehicle_type = VehicleType.objects.get(vehicle_type_name=vehicle_details['vehicle_type'])
            try:
                vehicle.vehicle_no = vehicle_details['vehicle_no']
                vehicle.plate_no = vehicle_details['plate_no']
                vehicle.vehicle_type_name = vehicle_type
                vehicle.vehicle_color = vehicle_details['color']
                vehicle.meter_reading = vehicle_details['meter_reading']
                vehicle.vehicle_condition = vehicle_details['condition']
                vehicle.insuranse_value = vehicle_details['insurance_value']
                vehicle.type_of_insuranse = vehicle_details['insurance_type']
                vehicle.save()
                res = {
                    'result': 'ok'
                }
                status = 200
            except Exception as ex:
                print "Exception == ", str(ex)
                res = {
                    'result': 'error',
                    'message': 'Vehicle with this Vehicle No. and Plate No. is already existing'
                }
                status = 500
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
            client = Client.objects.get(id=int(client_id))
            client_details = ast.literal_eval(request.POST['client_details'])
            try:
                client.phone_number = client_details['home_ph_no']
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
                
                client.passport_no = client_details['passport_no']
                client.date_of_passport_issue = datetime.strptime(client_details['passport_issued_date'], '%d/%m/%Y')
                client.place_of_issue = client_details['place_of_issue']

                client.save()
                res = {
                    'result': 'ok'
                }
                status = 200
            except Exception as ex:
                print "Exception == ", str(ex)
                res = {
                    'result': 'error',
                    'message': 'Client with this Passport No. and Tel No(Home). is already existing'
                }
                status = 500
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
                    rent_agreement.driver_name = rent_agreement_details['driver_name']
                    rent_agreement.driver_phone = rent_agreement_details['driver_phone']
                    rent_agreement.driver_address = rent_agreement_details['driver_address']
                    rent_agreement.driver_nationality = rent_agreement_details['nationality']
                    rent_agreement.driver_passport_no = rent_agreement_details['passport_no']
                    rent_agreement.driver_license_no = rent_agreement_details['license_no']
                    rent_agreement.driver_dob = datetime.strptime(rent_agreement_details['dob'], '%d/%m/%Y')
                    rent_agreement.driver_license_expiry_date = datetime.strptime(rent_agreement_details['license_expiry_date'], '%d/%m/%Y')
                    rent_agreement.driver_license_issue_place = rent_agreement_details['license_issued_place']
                    rent_agreement.driver_license_issue_date = datetime.strptime(rent_agreement_details['license_issued_date'], '%d/%m/%Y')
                    rent_agreement.sponsar_name = rent_agreement_details['sponsar_name']
                    rent_agreement.sponsar_address = rent_agreement_details['sponsar_telephone']
                    rent_agreement.sponsar_phone = rent_agreement_details['sponsar_address']
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

class AgreementDetails(View):

    def get(self, request, *args, **kwargs):

        agreement_no = request.GET.get('agreement_no', '')
        agreements = RentAgreement.objects.filter(is_completed=False, agreement_no__startswith=agreement_no)
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
                        'driver_name': agreement.driver_name,
                        'driver_passport_no': agreement.driver_passport_no,
                        'sponsar_name': agreement.sponsar_name,
                        'paid': agreement.paid,
                    })
            res = {
                'result': 'ok',
                'agreements': ctx_agreements,
            }
            status = 200
            response = simplejson.dumps(res)

            return HttpResponse(response, status=status, mimetype='application/json')
                    
