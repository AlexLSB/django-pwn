# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-20 11:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_pwn.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PWNOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last Name')),
                ('gender', models.CharField(choices=[(b'Male', 'Male'), (b'Female', 'Female')], max_length=255, verbose_name='Gender')),
                ('dob', models.CharField(help_text='YYYYMMDD', max_length=8, verbose_name='Date Of Birth')),
                ('state', models.CharField(help_text='2 letter abbreviation', max_length=2, verbose_name='State')),
                ('test_types', models.CharField(help_text='Comma separated list of order codes', max_length=255, verbose_name='Test Types')),
                ('test_groups', models.CharField(blank=True, help_text='Comma separated list of order group ids', max_length=255, null=True, verbose_name='Test Groups')),
                ('take_tests_same_day', models.BooleanField(default=False, verbose_name='Take tests same day')),
                ('home_phone', models.CharField(blank=True, help_text='At least one of home phone, work phone or mobile phone must be provided', max_length=255, null=True, validators=[django_pwn.models.validate_phone], verbose_name='Home Phone')),
                ('work_phone', models.CharField(blank=True, help_text='At least one of home phone, work phone or mobile phone must be provided', max_length=255, null=True, validators=[django_pwn.models.validate_phone], verbose_name='Work Phone')),
                ('mobile_phone', models.CharField(blank=True, help_text='At least one of home phone, work phone or mobile phone must be provided', max_length=255, null=True, validators=[django_pwn.models.validate_phone], verbose_name='Mobile Phone')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='City')),
                ('zip_code', models.CharField(max_length=255, verbose_name='ZIP code')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('email', models.CharField(max_length=255, verbose_name='E-mail')),
                ('draw_location', models.CharField(blank=True, choices=[('PSC', 'PSC'), ('Kit', 'Kit'), ('Visit', 'Visit'), ('HealthFair', 'Health Fair')], max_length=255, null=True, verbose_name='Draw location')),
                ('psc', models.CharField(blank=True, max_length=255, null=True, verbose_name='PSC')),
                ('reference', models.CharField(blank=True, max_length=255, null=True, verbose_name="Client's reference")),
                ('grouping', models.CharField(blank=True, max_length=255, null=True, verbose_name='Grouping')),
                ('validation_version', models.CharField(default='2', max_length=255, verbose_name='API validation version')),
                ('test_disclaimer_ids', models.CharField(blank=True, max_length=255, null=True, verbose_name='Disclaimer IDs')),
                ('primary_insurance', models.TextField(blank=True, null=True, verbose_name='Primary Insurance')),
                ('policy_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Policy number')),
                ('workers_compensation_flag', models.NullBooleanField(default=None)),
                ('secondary_insurance', models.TextField(blank=True, null=True, verbose_name='Secondary Insurance')),
                ('guarantor_info', models.TextField(blank=True, null=True, verbose_name='Guarantor Info')),
                ('relationship', models.IntegerField(blank=True, null=True, verbose_name='Relationship')),
                ('employer_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Employer name')),
                ('diagnosis_code', models.TextField(blank=True, null=True, verbose_name='Diagnosis code')),
                ('code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Actual diagnosis code')),
                ('reconciled_test_types', models.CharField(blank=True, max_length=255, null=True, verbose_name='Reconciled test types')),
                ('physicians_npi', models.CharField(blank=True, max_length=255, null=True, verbose_name='Physicians npi')),
                ('physicians_upin', models.CharField(blank=True, max_length=255, null=True, verbose_name='Physicians upin')),
                ('physicians_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Physicians name')),
                ('physicians_license', models.CharField(blank=True, max_length=255, null=True, verbose_name='Physicians physicians_license')),
                ('reconciled_results', models.TextField(blank=True, null=True, verbose_name='Reconciled results')),
                ('status', models.CharField(blank=True, max_length=255, null=True, verbose_name='status')),
                ('timestamp', models.CharField(blank=True, max_length=255, null=True, verbose_name='timestamp')),
                ('requisition_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Requisition number')),
                ('account_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Account number')),
                ('confirmation_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Confirmation code')),
                ('order_id', models.BigIntegerField(blank=True, null=True, verbose_name='Assotiated order id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('pwn_customer_created_at', models.DateTimeField(blank=True, null=True, verbose_name='PWN order created at')),
                ('pwn_customer_id', models.IntegerField(blank=True, db_index=True, help_text='Customer (order) ID in PWN system', null=True, unique=True, verbose_name='Customer ID')),
            ],
        ),
        migrations.CreateModel(
            name='PWNResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinical_info', models.CharField(blank=True, help_text='Contains the clinical info if such info was sent with the order', max_length=62, null=True)),
                ('collection_date', models.DateTimeField(null=True)),
                ('fasting', models.NullBooleanField()),
                ('lab_patient_id', models.CharField(max_length=255, null=True)),
                ('lab_report_release_date', models.DateTimeField(null=True)),
                ('receipt_date', models.DateTimeField(null=True)),
                ('reported_date', models.DateTimeField(null=True)),
                ('result_fasting', models.NullBooleanField()),
                ('lab_abnormal_flag', models.CharField(max_length=1, null=True)),
                ('lab_id', models.IntegerField(null=True)),
                ('lab_reference_range', models.CharField(max_length=255, null=True)),
                ('observation_date', models.DateTimeField(null=True)),
                ('order_lab_code', models.CharField(max_length=255, null=True)),
                ('order_lab_name', models.CharField(max_length=255, null=True)),
                ('result_lab_code', models.CharField(max_length=255, null=True)),
                ('result_lab_name', models.CharField(max_length=255, null=True)),
                ('result_status', models.CharField(max_length=1, null=True)),
                ('units_of_measurement', models.CharField(max_length=255, null=True)),
                ('value', models.CharField(max_length=255, null=True)),
                ('value_type', models.CharField(max_length=2, null=True)),
                ('notes', models.CharField(help_text='Holds the comments associated with test result', max_length=1000, null=True)),
                ('lab_facility', models.CharField(help_text='Laboratory info', max_length=255, null=True)),
                ('lab_facility_director', models.CharField(help_text='Laboratory medical director', max_length=255, null=True)),
                ('pwn_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='django_pwn.PWNOrder')),
            ],
        ),
    ]