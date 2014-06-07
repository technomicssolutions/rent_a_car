# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'RentAgreement.driver_license_no'
        db.delete_column(u'web_rentagreement', 'driver_license_no')

        # Deleting field 'RentAgreement.sponsar_phone'
        db.delete_column(u'web_rentagreement', 'sponsar_phone')

        # Deleting field 'RentAgreement.sponsar_address'
        db.delete_column(u'web_rentagreement', 'sponsar_address')

        # Deleting field 'RentAgreement.driver_passport_no'
        db.delete_column(u'web_rentagreement', 'driver_passport_no')

        # Deleting field 'RentAgreement.driver_dob'
        db.delete_column(u'web_rentagreement', 'driver_dob')

        # Deleting field 'RentAgreement.driver_phone'
        db.delete_column(u'web_rentagreement', 'driver_phone')

        # Deleting field 'RentAgreement.driver_name'
        db.delete_column(u'web_rentagreement', 'driver_name')

        # Deleting field 'RentAgreement.driver_license_issue_date'
        db.delete_column(u'web_rentagreement', 'driver_license_issue_date')

        # Deleting field 'RentAgreement.sponsar_name'
        db.delete_column(u'web_rentagreement', 'sponsar_name')

        # Deleting field 'RentAgreement.driver_license_expiry_date'
        db.delete_column(u'web_rentagreement', 'driver_license_expiry_date')

        # Deleting field 'RentAgreement.driver_nationality'
        db.delete_column(u'web_rentagreement', 'driver_nationality')

        # Deleting field 'RentAgreement.driver_license_issue_place'
        db.delete_column(u'web_rentagreement', 'driver_license_issue_place')

        # Deleting field 'RentAgreement.driver_address'
        db.delete_column(u'web_rentagreement', 'driver_address')

        # Adding field 'RentAgreement.driver'
        db.add_column(u'web_rentagreement', 'driver',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Driver'], null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'RentAgreement.driver_license_no'
        db.add_column(u'web_rentagreement', 'driver_license_no',
                      self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RentAgreement.sponsar_phone'
        db.add_column(u'web_rentagreement', 'sponsar_phone',
                      self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RentAgreement.sponsar_address'
        db.add_column(u'web_rentagreement', 'sponsar_address',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'RentAgreement.driver_passport_no'
        db.add_column(u'web_rentagreement', 'driver_passport_no',
                      self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RentAgreement.driver_dob'
        db.add_column(u'web_rentagreement', 'driver_dob',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'RentAgreement.driver_phone'
        db.add_column(u'web_rentagreement', 'driver_phone',
                      self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RentAgreement.driver_name'
        db.add_column(u'web_rentagreement', 'driver_name',
                      self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RentAgreement.driver_license_issue_date'
        db.add_column(u'web_rentagreement', 'driver_license_issue_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'RentAgreement.sponsar_name'
        db.add_column(u'web_rentagreement', 'sponsar_name',
                      self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RentAgreement.driver_license_expiry_date'
        db.add_column(u'web_rentagreement', 'driver_license_expiry_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'RentAgreement.driver_nationality'
        db.add_column(u'web_rentagreement', 'driver_nationality',
                      self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RentAgreement.driver_license_issue_place'
        db.add_column(u'web_rentagreement', 'driver_license_issue_place',
                      self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RentAgreement.driver_address'
        db.add_column(u'web_rentagreement', 'driver_address',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'RentAgreement.driver'
        db.delete_column(u'web_rentagreement', 'driver_id')

    models = {
        u'web.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'date_of_issue': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_passport_issue': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'expiry_license_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued_by': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'license_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'license_type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'passport_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'place_of_issue': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'rent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'work_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'work_ph_no': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'web.driver': {
            'Meta': {'object_name': 'Driver'},
            'driver_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'driver_dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'driver_license_expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'driver_license_issue_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'driver_license_issue_place': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'driver_license_no': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'driver_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'driver_nationality': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'driver_passport_no': ('django.db.models.fields.CharField', [], {'max_length': '25', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'driver_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sponsar_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sponsar_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'sponsar_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'web.receivecar': {
            'Meta': {'object_name': 'ReceiveCar'},
            'accident_passable': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'cheque_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'credit_card_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'extra_charge': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'fine': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_meter_reading': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'petrol': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'receipt_no': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'rent_agreement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.RentAgreement']", 'null': 'True', 'blank': 'True'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'type_of_fee': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        u'web.rentagreement': {
            'Meta': {'object_name': 'RentAgreement'},
            'agreement_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'agreement_no': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'agreement_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Client']", 'null': 'True', 'blank': 'True'}),
            'client_identity': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'commission': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'driver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Driver']", 'null': 'True', 'blank': 'True'}),
            'end_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity_driver': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'is_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'reduction': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'rent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'rent_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'starting_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'type_of_contract': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Vehicle']", 'null': 'True', 'blank': 'True'}),
            'with_driver': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'web.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insuranse_value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'meter_reading': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
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