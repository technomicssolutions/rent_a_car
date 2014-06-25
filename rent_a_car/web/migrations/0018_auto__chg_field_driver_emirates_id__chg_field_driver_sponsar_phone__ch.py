# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Driver.emirates_id'
        db.alter_column(u'web_driver', 'emirates_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Driver.sponsar_phone'
        db.alter_column(u'web_driver', 'sponsar_phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Driver.driver_working_ph'
        db.alter_column(u'web_driver', 'driver_working_ph', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Driver.driver_license_issue_place'
        db.alter_column(u'web_driver', 'driver_license_issue_place', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Driver.driver_nationality'
        db.alter_column(u'web_driver', 'driver_nationality', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Driver.driver_license_no'
        db.alter_column(u'web_driver', 'driver_license_no', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Driver.place_of_issue'
        db.alter_column(u'web_driver', 'place_of_issue', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Driver.driver_passport_no'
        db.alter_column(u'web_driver', 'driver_passport_no', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True))

        # Changing field 'Driver.driver_phone'
        db.alter_column(u'web_driver', 'driver_phone', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True))

        # Changing field 'Driver.sponsar_name'
        db.alter_column(u'web_driver', 'sponsar_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Driver.driver_name'
        db.alter_column(u'web_driver', 'driver_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))
    def backwards(self, orm):

        # Changing field 'Driver.emirates_id'
        db.alter_column(u'web_driver', 'emirates_id', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))

        # Changing field 'Driver.sponsar_phone'
        db.alter_column(u'web_driver', 'sponsar_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

        # Changing field 'Driver.driver_working_ph'
        db.alter_column(u'web_driver', 'driver_working_ph', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

        # Changing field 'Driver.driver_license_issue_place'
        db.alter_column(u'web_driver', 'driver_license_issue_place', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))

        # Changing field 'Driver.driver_nationality'
        db.alter_column(u'web_driver', 'driver_nationality', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))

        # Changing field 'Driver.driver_license_no'
        db.alter_column(u'web_driver', 'driver_license_no', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))

        # Changing field 'Driver.place_of_issue'
        db.alter_column(u'web_driver', 'place_of_issue', self.gf('django.db.models.fields.CharField')(max_length=40, null=True))

        # Changing field 'Driver.driver_passport_no'
        db.alter_column(u'web_driver', 'driver_passport_no', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25, null=True))

        # Changing field 'Driver.driver_phone'
        db.alter_column(u'web_driver', 'driver_phone', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15, null=True))

        # Changing field 'Driver.sponsar_name'
        db.alter_column(u'web_driver', 'sponsar_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))

        # Changing field 'Driver.driver_name'
        db.alter_column(u'web_driver', 'driver_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))
    models = {
        u'web.casedetail': {
            'Meta': {'object_name': 'CaseDetail'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Driver']", 'null': 'True', 'blank': 'True'}),
            'code_author': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'date_author': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fine_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_author': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'penality_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'penality_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'rent_agreement_reference_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'type_of_case': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Vehicle']", 'null': 'True', 'blank': 'True'}),
            'vehicle_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'web.driver': {
            'Meta': {'object_name': 'Driver'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'date_of_passport_issue': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'driver_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'driver_dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'driver_license_expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'driver_license_issue_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'driver_license_issue_place': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'driver_license_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'driver_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'driver_nationality': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'driver_passport_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'driver_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'driver_working_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'driver_working_ph': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'emirates_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license_type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'place_of_issue': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'sponsar_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sponsar_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sponsar_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'web.receivecar': {
            'Meta': {'object_name': 'ReceiveCar'},
            'cheque_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'credit_card_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'extra_charge': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'fine': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_meter_reading': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'petrol': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'receipt_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'receipt_no': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'reduction': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'rent_agreement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.RentAgreement']", 'null': 'True', 'blank': 'True'}),
            'returning_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'returning_petrol': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'salik_charges': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'type_of_fee': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        u'web.rentagreement': {
            'Meta': {'object_name': 'RentAgreement'},
            'accident_passable': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'agreement_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'agreement_no': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'client_identity': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'driver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Driver']", 'null': 'True', 'blank': 'True'}),
            'end_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity_driver': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'is_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'leaving_meterreading': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'leaving_petrol': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'liable_to_pay_in_km': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'rent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'rent_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'rental_entitled_in_km': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'starting_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Vehicle']", 'null': 'True', 'blank': 'True'}),
            'vehicle_scratch': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'})
        },
        u'web.typeofcase': {
            'Meta': {'object_name': 'TypeOfCase'},
            'case_type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'web.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insuranse_value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'meter_reading': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'petrol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'plate_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'type_of_insuranse': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'vehicle_color': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'vehicle_condition': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'vehicle_make': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'vehicle_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'vehicle_type_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.VehicleType']", 'null': 'True', 'blank': 'True'})
        },
        u'web.vehicletype': {
            'Meta': {'object_name': 'VehicleType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vehicle_type_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['web']