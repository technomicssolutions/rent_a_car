# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'web_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('nationality', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=15, unique=True, null=True, blank=True)),
            ('work_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('work_ph_no', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('license_no', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('license_type', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('date_of_issue', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('issued_by', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('expiry_license_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('passport_no', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True, null=True, blank=True)),
            ('date_of_passport_issue', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('place_of_issue', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('emirates_id', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('rent', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('paid', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'web', ['Client'])

        # Adding model 'VehicleType'
        db.create_table(u'web_vehicletype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vehicle_type_name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['VehicleType'])

        # Adding model 'Vehicle'
        db.create_table(u'web_vehicle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vehicle_no', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True, null=True, blank=True)),
            ('plate_no', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True, null=True, blank=True)),
            ('vehicle_make', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('vehicle_type_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.VehicleType'], null=True, blank=True)),
            ('vehicle_color', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('meter_reading', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('vehicle_condition', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('insuranse_value', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('type_of_insuranse', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'web', ['Vehicle'])

        # Adding model 'RentAgreement'
        db.create_table(u'web_rentagreement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vehicle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Vehicle'], null=True, blank=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Client'], null=True, blank=True)),
            ('agreement_no', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('agreement_type', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('agreement_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('starting_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('rent_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('identity_driver', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('client_identity', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('type_of_contract', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('driver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Driver'], null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('total_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('commission', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('reduction', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('rent', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('paid', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('is_completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'web', ['RentAgreement'])

        # Adding model 'ReceiveCar'
        db.create_table(u'web_receivecar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rent_agreement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.RentAgreement'], null=True, blank=True)),
            ('receipt_no', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('new_meter_reading', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('type_of_fee', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('petrol', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('fine', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('reduction', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('extra_charge', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('accident_passable', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('credit_card_no', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('cheque_no', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('total_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('paid', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['ReceiveCar'])

        # Adding model 'Driver'
        db.create_table(u'web_driver', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('driver_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('driver_phone', self.gf('django.db.models.fields.CharField')(max_length=15, unique=True, null=True, blank=True)),
            ('driver_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('driver_nationality', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('driver_passport_no', self.gf('django.db.models.fields.CharField')(max_length=25, unique=True, null=True, blank=True)),
            ('driver_license_no', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('driver_license_issue_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('driver_license_issue_place', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('driver_license_expiry_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('driver_dob', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('sponsar_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('sponsar_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sponsar_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'web', ['Driver'])

        # Adding model 'CaseDetail'
        db.create_table(u'web_casedetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vehicle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Vehicle'], null=True, blank=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Client'], null=True, blank=True)),
            ('fine_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('type_of_case', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('penality_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('penality_no', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('date_author', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('no_author', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('code_author', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['CaseDetail'])

        # Adding model 'TypeOfCase'
        db.create_table(u'web_typeofcase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('case_type', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['TypeOfCase'])

    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'web_client')

        # Deleting model 'VehicleType'
        db.delete_table(u'web_vehicletype')

        # Deleting model 'Vehicle'
        db.delete_table(u'web_vehicle')

        # Deleting model 'RentAgreement'
        db.delete_table(u'web_rentagreement')

        # Deleting model 'ReceiveCar'
        db.delete_table(u'web_receivecar')

        # Deleting model 'Driver'
        db.delete_table(u'web_driver')

        # Deleting model 'CaseDetail'
        db.delete_table(u'web_casedetail')

        # Deleting model 'TypeOfCase'
        db.delete_table(u'web_typeofcase')

    models = {
        u'web.casedetail': {
            'Meta': {'object_name': 'CaseDetail'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Client']", 'null': 'True', 'blank': 'True'}),
            'code_author': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'date_author': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fine_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_author': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'penality_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'penality_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'type_of_case': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Vehicle']", 'null': 'True', 'blank': 'True'})
        },
        u'web.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'date_of_issue': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_passport_issue': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'emirates_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
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
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'extra_charge': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'fine': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_meter_reading': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'petrol': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
            'receipt_no': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'reduction': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '25', 'decimal_places': '2'}),
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
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Vehicle']", 'null': 'True', 'blank': 'True'})
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