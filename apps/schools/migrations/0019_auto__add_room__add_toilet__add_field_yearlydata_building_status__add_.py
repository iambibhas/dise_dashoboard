# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Room'
        db.create_table(u'schools_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('yearly_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.YearlyData'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'schools', ['Room'])

        # Adding model 'Toilet'
        db.create_table(u'schools_toilet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('yearly_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.YearlyData'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'schools', ['Toilet'])

        # Adding field 'YearlyData.building_status'
        db.add_column(u'schools_yearlydata', 'building_status',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.SchoolBuildingStatus'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'YearlyData.room_count'
        db.add_column(u'schools_yearlydata', 'room_count',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Room'
        db.delete_table(u'schools_room')

        # Deleting model 'Toilet'
        db.delete_table(u'schools_toilet')

        # Deleting field 'YearlyData.building_status'
        db.delete_column(u'schools_yearlydata', 'building_status_id')

        # Deleting field 'YearlyData.room_count'
        db.delete_column(u'schools_yearlydata', 'room_count')


    models = {
        u'common.block': {
            'Meta': {'object_name': 'Block'},
            'education_district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.EducationDistrict']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'common.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Block']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'common.educationdistrict': {
            'Meta': {'object_name': 'EducationDistrict'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.State']", 'null': 'True', 'blank': 'True'})
        },
        u'common.state': {
            'Meta': {'object_name': 'State'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'common.village': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Village'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'schools.academicyear': {
            'Meta': {'object_name': 'AcademicYear'},
            'from_year': ('django.db.models.fields.SmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_year': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'schools.boundarywalltype': {
            'Meta': {'object_name': 'BoundaryWallType'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'schools.drinkingwatersource': {
            'Meta': {'object_name': 'DrinkingWaterSource'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'schools.instractionmedium': {
            'Meta': {'object_name': 'InstractionMedium'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'schools.residentialtype': {
            'Meta': {'object_name': 'ResidentialType'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'schools.room': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Room'},
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'yearly_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.YearlyData']"})
        },
        u'schools.school': {
            'Meta': {'ordering': "('id',)", 'object_name': 'School'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'pincode': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year_established': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'schools.schoolbuildingstatus': {
            'Meta': {'object_name': 'SchoolBuildingStatus'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'schools.schoolcategory': {
            'Meta': {'object_name': 'SchoolCategory'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'schools.schoolmanaagement': {
            'Meta': {'object_name': 'SchoolManaagement'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'schools.toilet': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Toilet'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'yearly_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.YearlyData']"})
        },
        u'schools.yearlydata': {
            'Meta': {'ordering': "('id',)", 'object_name': 'YearlyData'},
            'academic_inspection_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'academic_year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.AcademicYear']"}),
            'area_type': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'brc_visit_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'building_status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.SchoolBuildingStatus']", 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.SchoolCategory']", 'null': 'True', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Cluster']", 'null': 'True', 'blank': 'True'}),
            'crc_visit_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'development_grant_expenditure': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'development_grant_received': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'distance_from_brc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'distance_from_crc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fund_from_student_expenditure': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fund_from_student_received': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'highest_class': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lowest_class': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'management': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.SchoolManaagement']", 'null': 'True', 'blank': 'True'}),
            'mediums': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['schools.InstractionMedium']", 'null': 'True', 'blank': 'True'}),
            'part_of_shift': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pre_primary_available': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pre_primary_student_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pre_primary_teacher_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'residential': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'residential_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.ResidentialType']", 'null': 'True', 'blank': 'True'}),
            'room_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.School']"}),
            'tlm_grant_expenditure': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tlm_grant_received': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Village']", 'null': 'True', 'blank': 'True'}),
            'ward_no': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'working_day_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['schools']