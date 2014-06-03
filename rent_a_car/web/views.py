import simplejson
import ast
from datetime import datetime

from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

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
                        'client_name': client.name,
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
            vehicle, created = Vehicle.objects.get_or_create(vehicle_no=vehicle_details['vehicle_no'],plate_no=vehicle_details['plate_no'])
            if created:
                
                vehicle_type, vehicle_created = VehicleType.objects.get_or_create(vehicle_type_name=vehicle_details['vehicle_type'])
                vehicle.vehicle_type_name = vehicle_type
                vehicle.vehicle_color = vehicle_details['color']
                vehicle.meter_reading = vehicle_details['meter_reading']
                vehicle.vehicle_condition = vehicle_details['condition']
                vehicle.insuranse_value = vehicle_details['insurense_value']
                vehicle.type_of_insuranse = vehicle_details['insurance_type']
                vehicle.save()
                res = {
                    'result': 'ok',
                }
                status = 200

            else:

                res = {
                    'result': 'error',
                    'message': 'Vehicle with this Vehicle no and Plate No. is already existing'
                }
                status = 500

            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')



class Vehicles(View):

    def get(self, request, *args, **kwargs):

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



