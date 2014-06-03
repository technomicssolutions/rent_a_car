# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Vehicle', fields ['plate_no']
        db.create_unique(u'web_vehicle', ['plate_no'])

        # Adding unique constraint on 'Vehicle', fields ['vehicle_no']
        db.create_unique(u'web_vehicle', ['vehicle_no'])

    def backwards(self, orm):
        # Removing unique constraint on 'Vehicle', fields ['vehicle_no']
        db.delete_unique(u'web_vehicle', ['vehicle_no'])

        # Removing unique constraint on 'Vehicle', fields ['plate_no']
        db.delete_unique(u'web_vehicle', ['plate_no'])

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
            'meter_reading': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'plate_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'type_of_insurense': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'vehicle_color': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
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