# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RentAgreement'
        db.create_table(u'web_rentagreement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vehicle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Vehicle'], null=True, blank=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Client'], null=True, blank=True)),
            ('agreement_no', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('agreement_type', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('agreement_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('starting_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('rent_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('identity_driver', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('client_identity', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('driver_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('driver_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('driver_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sponsar_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('sponsar_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sponsar_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['RentAgreement'])

        # Adding field 'Vehicle.is_available'
        db.add_column(u'web_vehicle', 'is_available',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting model 'RentAgreement'
        db.delete_table(u'web_rentagreement')

        # Deleting field 'Vehicle.is_available'
        db.delete_column(u'web_vehicle', 'is_available')

    models = {
        u'web.client': {
            'Meta': {'unique_together': "(('passport_no', 'phone_number'),)", 'object_name': 'Client'},
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
            'passport_no': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'place_of_issue': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'rent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'work_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'work_ph_no': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'web.rentagreement': {
            'Meta': {'object_name': 'RentAgreement'},
            'agreement_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'agreement_no': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'agreement_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Client']", 'null': 'True', 'blank': 'True'}),
            'client_identity': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'driver_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'driver_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'driver_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity_driver': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rent_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'sponsar_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sponsar_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'sponsar_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'starting_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Vehicle']", 'null': 'True', 'blank': 'True'})
        },
        u'web.vehicle': {
            'Meta': {'unique_together': "(('vehicle_no', 'plate_no'),)", 'object_name': 'Vehicle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insuranse_value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'meter_reading': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'plate_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'type_of_insuranse': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'vehicle_color': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'vehicle_condition': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'vehicle_make': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'vehicle_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'vehicle_type_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.VehicleType']", 'null': 'True', 'blank': 'True'})
        },
        u'web.vehicletype': {
            'Meta': {'object_name': 'VehicleType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vehicle_type_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['web']