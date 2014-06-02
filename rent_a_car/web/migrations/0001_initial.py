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
            ('passport_no', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('date_of_passport_issue', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('place_of_issue', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('deposit_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('rent', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('paid', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'web', ['Client'])

        # Adding model 'Vehicle'
        db.create_table(u'web_vehicle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vehicle_no', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('plate_no', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('vehicle_make', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('vehicle_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('vehicle_color', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('insurense_value', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('type_of_insurense', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Vehicle'])

    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'web_client')

        # Deleting model 'Vehicle'
        db.delete_table(u'web_vehicle')

    models = {
        u'web.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'date_of_issue': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_passport_issue': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deposit_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'expiry_license_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued_by': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'license_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'license_type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'passport_no': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'place_of_issue': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'rent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'work_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'work_ph_no': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'web.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurense_value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'plate_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'type_of_insurense': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'vehicle_color': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'vehicle_make': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'vehicle_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'vehicle_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['web']