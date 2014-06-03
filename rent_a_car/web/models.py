from django.db import models

# Create your models here.
LICENSE_TYPE = (
    ('automatic', 'automatic'),
    ('manual', 'manual'),
    ('heavy', 'heavy'),
)

class Client(models.Model):

    # Personal Details
    name = models.CharField('Name of the Client', max_length=75, null=True, blank=True)
    address = models.TextField('Address', null=True, blank=True)
    nationality = models.CharField('Nationality', null=True, blank=True, max_length=50)
    dob = models.DateField('Date of Birth', null=True, blank=True)
    phone_number = models.CharField('Phone number', max_length=15, null=True, blank=True, unique=True)
    work_address = models.TextField('Work Address', null=True, blank=True)
    work_ph_no = models.CharField('Phone no.(Work)', max_length=15, null=True, blank=True)

    # License Details
    license_no = models.CharField('License No.', max_length=30, null=True, blank=True)
    license_type = models.CharField('License Type', max_length=40, null=True, blank=True, choices=LICENSE_TYPE)
    date_of_issue = models.DateField('Date of Issue', null=True, blank=True)
    issued_by = models.CharField('Issued By', null=True, blank=True, max_length=50)
    expiry_license_date = models.DateField('Expiry Date', null=True, blank=True)

    # Passport Details
    passport_no = models.CharField('Passport Number', unique=True, max_length=30)
    date_of_passport_issue = models.DateField('Date of Passport Issued', null=True, blank=True)
    place_of_issue = models.CharField('Place of Issued', null=True, blank=True, max_length=40)

    # Rent Details
    # deposit_amount = models.DecimalField('Deposit Amount', default=0, max_digits=14, decimal_places=2)
    rent = models.DecimalField('Rent Amount(Deposit)', default=0, max_digits=14, decimal_places=2)
    paid = models.DecimalField('Paid', default=0, max_digits=14, decimal_places=2)
    balance = models.DecimalField('Balance', default=0, max_digits=14, decimal_places=2)


    def __unicode__(self):

        return str(self.name)

    class Meta:

        verbose_name = 'Client'
        verbose_name_plural = 'Client'

class VehicleType(models.Model):

    vehicle_type_name = models.CharField('Vehicle Type', max_length=20, null=True, blank=True)

    def __unicode__(self):

        return self.vehicle_type_name

    class Meta:

        verbose_name = 'Vehicle Type'
        verbose_name_plural = 'Vehicle Type'

class Vehicle(models.Model):

    vehicle_no = models.CharField('Vehicle No', null=True, blank=True, max_length=20)
    plate_no = models.CharField('Plate No', null=True, blank=True, max_length=20)
    vehicle_make = models.CharField('Vehicle Make', null=True, blank=True, max_length=25)
    vehicle_type_name = models.ForeignKey(VehicleType, null=True, blank=True)
    vehicle_color = models.CharField('Vehicle Color', null=True, blank=True, max_length=25)
    meter_reading = models.CharField('Meter Reading', null=True, blank=True, max_length=25)
    vehicle_condition = models.CharField('Vehicle Condition', null=True, blank=True, max_length=30)

    # Insurance Details 
    insuranse_value = models.DecimalField('Insurance Value', default=0, max_digits=14, decimal_places=2)
    type_of_insuranse = models.CharField('Type of Insurance', null=True, blank=True, max_length=20)


    def __unicode__(self):

        return str(self.vehicle_no)

    class Meta:

        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicle'
        unique_together = ('vehicle_no', 'plate_no')