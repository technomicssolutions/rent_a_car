from django.db import models

# Create your models here.
LICENSE_TYPE = (
    ('automatic', 'automatic'),
    ('manual', 'manual'),
    ('heavy', 'heavy'),
)

CLIENT_IDENTITY = (
    ('Emiratesid', 'Emiratesid'),
    ('Passport', 'Passport'),
    ('Driving License', 'Driving License'),
)

RENT_TYPE = (
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
)


class VehicleType(models.Model):

    vehicle_type_name = models.CharField('Vehicle Type', max_length=20, null=True, blank=True)

    def __unicode__(self):

        return self.vehicle_type_name

    class Meta:

        verbose_name = 'Vehicle Type'
        verbose_name_plural = 'Vehicle Type'

class Vehicle(models.Model):

    vehicle_no = models.CharField('Vehicle No', null=True, blank=True, max_length=20, unique=True)
    plate_no = models.CharField('Plate No', null=True, blank=True, max_length=20, unique=True)
    vehicle_make = models.CharField('Vehicle Make', null=True, blank=True, max_length=25)
    vehicle_type_name = models.ForeignKey(VehicleType, null=True, blank=True)
    vehicle_color = models.CharField('Vehicle Color', null=True, blank=True, max_length=25)
    meter_reading = models.CharField('Meter Reading', null=True, blank=True, max_length=25)
    vehicle_condition = models.CharField('Vehicle Condition', null=True, blank=True, max_length=30)
    petrol = models.CharField('Petrol', max_length=20, null=True, blank=True)

    # Insurance Details 
    insuranse_value = models.DecimalField('Insurance Value', default=0, max_digits=14, decimal_places=2)
    type_of_insuranse = models.CharField('Type of Insurance', null=True, blank=True, max_length=20)
    is_available = models.BooleanField('Is Available', default=True)


    def __unicode__(self):

        return str(self.vehicle_no)

    class Meta:

        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicle'

class RentAgreement(models.Model):

    vehicle = models.ForeignKey(Vehicle, null=True, blank=True)
    
    agreement_no = models.CharField('Agreement No.', null=True, blank=True, max_length=25)
    agreement_date = models.DateField('Agreement Date', null=True, blank=True)
    starting_date_time = models.DateTimeField('Starting Date and Time', null=True, blank=True)
    end_date_time = models.DateTimeField('End Date and Time', null=True, blank=True)
    rent_type = models.CharField('Rent Type', null=True, blank=True, max_length=25, choices=RENT_TYPE)

    rental_entitled_in_km = models.CharField('Rental Entitled in KM', max_length=25, null=True, blank=True)
    liable_to_pay_in_km = models.CharField('Liable to Pay in KM', max_length=25, null=True, blank=True)
    
    identity_driver = models.CharField('Identity Driver', null=True, blank=True, max_length=35)
    client_identity = models.CharField('Cleint Identity', null=True, blank=True, max_length=25, choices=CLIENT_IDENTITY)
    
    driver = models.ForeignKey('Driver', null=True, blank=True)
    notes = models.TextField('Notes', null=True, blank=True)

    total_amount = models.DecimalField('Amount', decimal_places=2, max_digits=25, default=0)
    rent = models.DecimalField('Rent', max_digits=25, decimal_places=2, default=0)
    paid = models.DecimalField('Deposit', max_digits=25, decimal_places=2, default=0)

    leaving_meterreading = models.CharField('Meter Reading', null=True, blank=True, max_length=20)
    leaving_petrol = models.CharField('Leaving Petrol', max_length=25, null=True, blank=True)

    vehicle_scratch = models.DecimalField('Vehicle Scratch', max_digits=25, decimal_places=2, default=0)
    accident_passable = models.DecimalField('Accident Passable', max_digits=25, decimal_places=2, default=0)

    is_completed = models.BooleanField('Completed', default=False)

    def __unicode__(self):

        return str(self.agreement_no)

    class Meta:

        verbose_name = 'Rent Agreement'
        verbose_name_plural = 'Rent Agreement'

class ReceiveCar(models.Model):

    rent_agreement = models.ForeignKey(RentAgreement, null=True, blank=True)

    receipt_no = models.CharField('Receipt No', null=True, blank=True, max_length=10)
    new_meter_reading = models.CharField('Meter Reading', null=True, blank=True, max_length=25)
    type_of_fee = models.CharField('Type of Fee', max_length=40, null=True, blank=True)
    receipt_datetime = models.DateTimeField('Receipt Date Time', null=True, blank=True)
    returning_date_time = models.DateTimeField('Returning Date Time', null=True, blank=True)
    
    petrol = models.DecimalField('Petrol', max_digits=25, decimal_places=2, default=0)
    
    fine = models.DecimalField('Fine', max_digits=25, decimal_places=2, default=0)
    reduction = models.DecimalField('Reduction', max_digits=25, decimal_places=2, default=0)
    extra_charge = models.DecimalField('Extra Charge', max_digits=25, decimal_places=2, default=0)
    salik_charges = models.DecimalField('Salik Charges', max_digits=25, decimal_places=2, default=0)
    
    credit_card_no = models.CharField('Credit card no', max_length=20, null=True, blank=True)
    cheque_no = models.CharField('Cheque no', null=True, blank=True, max_length=20)

    total_amount = models.DecimalField('Total Amount', decimal_places=2, max_digits=25, default=0)
    paid = models.DecimalField('Paid on receipt', decimal_places=2, max_digits=25, default=0)

    returning_petrol = models.CharField('Returning Petrol', max_length=25, null=True, blank=True)

    notes = models.TextField('Notes', null=True, blank=True)

    def __unicode__(self):

        return str(self.receipt_no)

    class Meta:

        verbose_name = 'Receive Car'
        verbose_name_plural = 'Receive Car'

class Driver(models.Model):

    driver_name = models.CharField('Driver Name', null=True, blank=True, max_length=25)
    driver_phone = models.CharField('Driver Phone', null=True, blank=True, max_length=15, unique=True)
    driver_address = models.TextField('Driver Address', null=True, blank=True)
    driver_nationality = models.CharField('Driver Nationality', null=True, blank=True, max_length=25)
    driver_passport_no = models.CharField('Driver Passport No', null=True, blank=True, max_length=25, unique=True)
    driver_license_no = models.CharField('Driver License No', null=True, blank=True, max_length=25)
    driver_license_issue_date = models.DateField('Driver License Issue Date', null=True, blank=True)
    driver_license_issue_place = models.CharField('Driver License Issue Place', null=True, blank=True, max_length=25)
    driver_license_expiry_date = models.DateField('Driver License Expiry Date', null=True, blank=True)
    driver_dob = models.DateField('Driver DOB', null=True, blank=True)
    driver_working_address = models.TextField('Driver Working address', null=True, blank=True)
    driver_working_ph = models.CharField('Driver Working Ph No.', null=True, blank=True, max_length=15)

    sponsar_name = models.CharField('Sponsar Name', null=True, blank=True, max_length=25)
    sponsar_address = models.TextField('Sponsar Address', null=True, blank=True)
    sponsar_phone = models.CharField('Sponsar Phone', null=True, blank=True, max_length=15)
    
    license_type = models.CharField('License Type', max_length=40, null=True, blank=True, choices=LICENSE_TYPE)
    # # Passport Details
    date_of_passport_issue = models.DateField('Date of Passport Issued', null=True, blank=True)
    place_of_issue = models.CharField('Place of Issued', null=True, blank=True, max_length=40)

    emirates_id = models.CharField('Emiratesid', max_length=25, null=True, blank=True)

    # # Rent Details
    rent = models.DecimalField('Rent Amount(Deposit)', default=0, max_digits=14, decimal_places=2)
    paid = models.DecimalField('Paid', default=0, max_digits=14, decimal_places=2)
    balance = models.DecimalField('Balance', default=0, max_digits=14, decimal_places=2)

    def __unicode__(self):

        return str(self.driver_name)

    class Meta:

        verbose_name = 'Driver'
        verbose_name_plural = 'Driver'

class CaseDetail(models.Model):

    vehicle = models.ForeignKey(Vehicle, null=True, blank=True)
    client = models.ForeignKey(Driver, null=True, blank=True)

    vehicle_status = models.CharField('Vehicle Status', null=True, blank=True, max_length=20)
    rent_agreement_reference_no = models.CharField('Reference No', null=True, blank=True, max_length=20)
    fine_amount = models.DecimalField('Fine Amount', decimal_places=2, max_digits=25, default=0)
    type_of_case = models.CharField('Type of Case', max_length=25, null=True, blank=True)
    penality_date = models.DateField('Penality Date', null=True, blank=True)
    penality_no = models.CharField('Penality No', null=True, blank=True, max_length=20)
    date_author = models.DateField('Date Author', null=True, blank=True)
    no_author = models.CharField('No Author', max_length=30, null=True, blank=True)
    code_author = models.CharField('Code Author', max_length=30, null=True, blank=True)

    def __unicode__(self):

        return str(self.vehicle.vehicle_no)


    class Meta:

        verbose_name = 'Case Details'
        verbose_name_plural = 'Case Details'

class TypeOfCase(models.Model):

    case_type = models.CharField('Case Type', max_length=40, null=True, blank=True)

    def __unicode__(self):

        return self.case_type

    class Meta:

        verbose_name = 'Case Type'
        verbose_name_plural = 'Case Type'