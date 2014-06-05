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
    phone_number = models.CharField('Phone number', max_length=15, null=True, blank=True)
    work_address = models.TextField('Work Address', null=True, blank=True)
    work_ph_no = models.CharField('Phone no.(Work)', max_length=15, null=True, blank=True)

    # License Details
    license_no = models.CharField('License No.', max_length=30, null=True, blank=True)
    license_type = models.CharField('License Type', max_length=40, null=True, blank=True, choices=LICENSE_TYPE)
    date_of_issue = models.DateField('Date of Issue', null=True, blank=True)
    issued_by = models.CharField('Issued By', null=True, blank=True, max_length=50)
    expiry_license_date = models.DateField('Expiry Date', null=True, blank=True)

    # Passport Details
    passport_no = models.CharField('Passport Number', max_length=30)
    date_of_passport_issue = models.DateField('Date of Passport Issued', null=True, blank=True)
    place_of_issue = models.CharField('Place of Issued', null=True, blank=True, max_length=40)

    # Rent Details
    rent = models.DecimalField('Rent Amount(Deposit)', default=0, max_digits=14, decimal_places=2)
    paid = models.DecimalField('Paid', default=0, max_digits=14, decimal_places=2)
    balance = models.DecimalField('Balance', default=0, max_digits=14, decimal_places=2)



    def __unicode__(self):

        return str(self.name)

    class Meta:

        verbose_name = 'Client'
        verbose_name_plural = 'Client'
        unique_together = ('passport_no', 'phone_number')


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
    is_available = models.BooleanField('Is Available', default=True)


    def __unicode__(self):

        return str(self.vehicle_no)

    class Meta:

        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicle'
        unique_together = ('vehicle_no', 'plate_no')

class RentAgreement(models.Model):

    vehicle = models.ForeignKey(Vehicle, null=True, blank=True)
    client = models.ForeignKey(Client, null=True, blank=True)
    
    agreement_no = models.CharField('Agreement No.', null=True, blank=True, max_length=25)
    agreement_type = models.CharField('Agreement Type', null=True, blank=True, max_length=30)
    agreement_date = models.DateField('Agreement Date', null=True, blank=True)
    starting_date_time = models.DateTimeField('Starting Date and Time', null=True, blank=True)
    end_date_time = models.DateTimeField('End Date and Time', null=True, blank=True)
    rent_type = models.CharField('Rent Type', null=True, blank=True, max_length=25)
    
    identity_driver = models.CharField('Identity Driver', null=True, blank=True, max_length=35)
    client_identity = models.CharField('Cleint Identity', null=True, blank=True, max_length=25)
    with_driver = models.BooleanField('With Driver', default=False)
    
    type_of_contract = models.CharField('Type of Contract', null=True, blank=True, max_length=25)
    driver_name = models.CharField('Driver Name', null=True, blank=True, max_length=25)
    driver_phone = models.CharField('Driver Phone', null=True, blank=True, max_length=15)
    driver_address = models.TextField('Driver Address', null=True, blank=True)
    driver_nationality = models.CharField('Driver Nationality', null=True, blank=True, max_length=25)
    driver_passport_no = models.CharField('Driver Passport No', null=True, blank=True, max_length=25)
    driver_license_no = models.CharField('Driver License No', null=True, blank=True, max_length=25)
    driver_license_issue_date = models.DateField('Driver License Issue Date', null=True, blank=True)
    driver_license_issue_place = models.CharField('Driver License Issue Place', null=True, blank=True, max_length=25)
    driver_license_expiry_date = models.DateField('Driver License Expiry Date', null=True, blank=True)
    driver_dob = models.DateField('Driver DOB', null=True, blank=True)

    sponsar_name = models.CharField('Sponsar Name', null=True, blank=True, max_length=25)
    sponsar_address = models.TextField('Sponsar Address', null=True, blank=True)
    sponsar_phone = models.CharField('Sponsar Phone', null=True, blank=True, max_length=15)
    notes = models.TextField('Notes', null=True, blank=True)

    total_amount = models.DecimalField('Amount', decimal_places=2, max_digits=25, default=0)
    commission = models.DecimalField('Commission', max_digits=25, decimal_places=2, default=0)
    reduction = models.DecimalField('Reduction', max_digits=25, decimal_places=2, default=0)
    rent = models.DecimalField('Rent', max_digits=25, decimal_places=2, default=0)
    paid = models.DecimalField('Paid', max_digits=25, decimal_places=2, default=0)
    
    

    def __unicode__(self):

        return str(self.agreement_no)

    class Meta:

        verbose_name = 'Rent Agreement'
        verbose_name_plural = 'Rent Agreement'