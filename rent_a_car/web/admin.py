from django.contrib import admin
from web.models import *

admin.site.register(Client)
admin.site.register(VehicleType)
admin.site.register(Vehicle)
admin.site.register(RentAgreement)
admin.site.register(ReceiveCar)
admin.site.register(CaseDetail)
admin.site.register(Driver)

