from __future__ import unicode_literals

import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import dateutil.parser

import utils
from api import GENDER_FEMALE, GENDER_MALE, PWNAPIResource


api = PWNAPIResource()

CUSTOMER_TAG_NAMES = [
    "id", "timestamp", "status", "requisition_number", "account_number",
    "confirmation_code", "first_name", "last_name", "gender", "dob", "state",
    "test_types", "test_groups", "reconciled_test_types", "home_phone", "work_phone",
    "mobile_phone", "zip", "city", "address", "email", "draw_location", "psc", "reference",
    "grouping", "physicians_name", "physicians_upin", "physicians_npi", "physicians_license",
    "reconciled_results", "first_name", "last_name", "dob", "gender", "test_types", "state",
    "address", "email",]


def validate_phone(value):
    """
        Phone validation to meet the PWN requirements
    """
    reg = re.compile("^[01]?[- .]?\(?[2-9]\d{2}\)?[- .]?\d{3}[- .]?\d{4}$")
    if not reg.match(value):
        raise ValidationError(u"%s phone does not comply" % value)


def validate_email(value):
    """
        Email validation to meet the PWN requirements
    """
    reg = re.compile("/^([^@\s]+)@((?:[-a-z0-9]+\.)+[a-z]{2,})$/i")
    if not reg.match(value):
        raise ValidationError(u"%s email does not comply" % value)


def none_or_boolean(value):
    if value == 'true':
        return True
    elif value == 'false':
        return False
    else:
        return None


def convert_datetime(value):
    if not value:
        return None
    date_in_string = value.get('text', None)
    if date_in_string:
        return dateutil.parser.parse(date_in_string)
    else:
        return None


@python_2_unicode_compatible
class PWNOrder(models.Model):
    """
        Wraps PWN API, saves request data to database
    Usage::
        >>> order = PWNOrder({"count": 5})
        >>> order.create()     # return True or False

        More info at https://api-docs-labs-module.pwnhealth.com/v3.2.0/reference#post-customers
    """

    GENDER_MALE = GENDER_MALE
    GENDER_FEMALE = GENDER_FEMALE
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    )
    DRAW_LOCATION_PSC = "PSC"
    DRAW_LOCATION_KIT = "Kit"
    DRAW_LOCATION_VISIT = "Visit"
    DRAW_LOCATION_HEALTH_FAIR = "HealthFair"
    DRAW_LOCATION_CHOICES = (
        (DRAW_LOCATION_PSC, "PSC"),
        (DRAW_LOCATION_KIT, "Kit"),
        (DRAW_LOCATION_VISIT, "Visit"),
        (DRAW_LOCATION_HEALTH_FAIR, "Health Fair")
    )

    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'gender',
        'dob',
        'state',
        'zip_code',
        'address',
        'email',
    ]

    first_name = models.CharField(verbose_name=u"First Name", max_length=255)
    last_name = models.CharField(verbose_name=u"Last Name", max_length=255)
    gender = models.CharField(
        verbose_name=u"Gender", max_length=255,
        choices=GENDER_CHOICES)
    dob = models.CharField(verbose_name=u"Date Of Birth", max_length=8, help_text=u"YYYYMMDD")
    state = models.CharField(verbose_name=u"State", max_length=2, help_text=u"2 letter abbreviation")
    test_types = models.CharField(verbose_name=u"Test Types", max_length=255, help_text=u"Comma separated list of order codes")
    test_groups = models.CharField(verbose_name=u"Test Groups", max_length=255, help_text=u"Comma separated list of order group ids", null=True, blank=True)
    take_tests_same_day = models.BooleanField(verbose_name=u"Take tests same day", default=False)
    home_phone = models.CharField(
        verbose_name=u"Home Phone", max_length=255,
        validators=[validate_phone],
        help_text=u"At least one of home phone, work phone or mobile phone must be provided",
        null=True, blank=True)
    work_phone = models.CharField(
        verbose_name=u"Work Phone", max_length=255,
        validators=[validate_phone],
        help_text=u"At least one of home phone, work phone or mobile phone must be provided",
        null=True, blank=True)
    mobile_phone = models.CharField(
        verbose_name=u"Mobile Phone", max_length=255,
        validators=[validate_phone],
        help_text=u"At least one of home phone, work phone or mobile phone must be provided",
        null=True, blank=True)
    city = models.CharField(verbose_name=u"City", max_length=255, null=True, blank=True)
    zip_code = models.CharField(verbose_name=u"ZIP code", max_length=255)
    address = models.CharField(verbose_name=u"Address", max_length=255)
    email = models.CharField(
        verbose_name=u"E-mail",
        # validators=[validate_email],
        max_length=255)
    draw_location = models.CharField(
        verbose_name=u"Draw location", max_length=255, null=True, blank=True,
        choices=DRAW_LOCATION_CHOICES)
    psc = models.CharField(verbose_name=u"PSC", max_length=255, null=True, blank=True)
    reference = models.CharField(verbose_name=u"Client's reference", max_length=255, null=True, blank=True)
    grouping = models.CharField(verbose_name=u"Grouping", max_length=255, null=True, blank=True)
    validation_version = models.CharField(verbose_name=u"API validation version", max_length=255, default="2")
    test_disclaimer_ids = models.CharField(verbose_name=u"Disclaimer IDs", max_length=255, null=True, blank=True)
    primary_insurance = models.TextField(verbose_name=u"Primary Insurance", null=True, blank=True)
    policy_number = models.CharField(verbose_name=u"Policy number", max_length=255, null=True, blank=True)
    workers_compensation_flag = models.NullBooleanField(default=None)
    secondary_insurance = models.TextField(verbose_name=u"Secondary Insurance", null=True, blank=True)
    guarantor_info = models.TextField(verbose_name=u"Guarantor Info", null=True, blank=True)
    relationship = models.IntegerField(verbose_name=u"Relationship", null=True, blank=True)
    employer_name = models.CharField(verbose_name=u"Employer name", max_length=255, null=True, blank=True)
    diagnosis_code = models.TextField(verbose_name=u"Diagnosis code", null=True, blank=True)
    code = models.CharField(verbose_name=u"Actual diagnosis code", max_length=255, null=True, blank=True)

    reconciled_test_types = models.CharField(verbose_name=u"Reconciled test types", max_length=255, null=True, blank=True)
    physicians_npi = models.CharField(verbose_name=u"Physicians npi", max_length=255, null=True, blank=True)
    physicians_upin = models.CharField(verbose_name=u"Physicians upin", max_length=255, null=True, blank=True)
    physicians_name = models.CharField(verbose_name=u"Physicians name", max_length=255, null=True, blank=True)
    physicians_license = models.CharField(verbose_name=u"Physicians physicians_license", max_length=255, null=True, blank=True)
    reconciled_results = models.TextField(verbose_name=u"Reconciled results", null=True, blank=True)
    status = models.CharField(verbose_name=u"status", max_length=255, null=True, blank=True)
    timestamp = models.CharField(verbose_name=u"timestamp", max_length=255, null=True, blank=True)
    requisition_number = models.CharField(verbose_name=u"Requisition number", max_length=255, null=True, blank=True)
    account_number = models.CharField(verbose_name=u"Account number", max_length=255, null=True, blank=True)
    confirmation_code = models.CharField(verbose_name=u"Confirmation code", max_length=255, null=True, blank=True)

    order_id = models.BigIntegerField(verbose_name=u"Assotiated order id", null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=u"Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u"Modified at", auto_now=True)
    pwn_customer_created_at = models.DateTimeField(verbose_name=u"PWN order created at", null=True, blank=True)
    pwn_customer_id = models.IntegerField(
        verbose_name=u"Customer ID",
        help_text=u"Customer (order) ID in PWN system", null=True, blank=True, db_index=True, unique=True)

    def __str__(self):
        return _("PWNOrder #%s for %s %s") % (
            self.pk, self.first_name, self.last_name)

    def clean(self):
        if not self.test_types:
            raise ValidationError("Test types cannot be empty!")

    def save(self, *args, **kwargs):
        self.full_clean()
        super(PWNOrder, self).save(*args, **kwargs)

    def create(self):
        self.save()
        pwn_order = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "dob": self.dob,
            "state": self.state,
            "zip_code": self.zip_code,
            "city": self.city,
            "test_types": self.test_types,
            "take_tests_same_day": self.take_tests_same_day,
            "email": self.email,
            "address": self.address,
            "work_phone": self.work_phone
        }
        pwn_response = api.create_customer(**pwn_order)
        self.pwn_customer_created_at = timezone.now()
        self.requisition_number = pwn_response.requisition_number.text
        self.account_number = pwn_response.account_number.text
        self.confirmation_code = pwn_response.confirmation_code.text
        self.reconciled_test_types = pwn_response.reconciled_test_types.text
        self.draw_location = pwn_response.draw_location.text
        self.physicians_name = pwn_response.physicians_name.text
        self.physicians_upin = pwn_response.physicians_upin.text
        self.physicians_npi = pwn_response.physicians_npi.text
        self.physicians_license = pwn_response.physicians_license.text
        self.status = pwn_response.status.text
        self.timestamp = pwn_response.timestamp.text
        self.pwn_customer_id = pwn_response.id.text
        self.save()
        return bool(self.pwn_customer_id)

    def save_results(self):
        pwn_order = utils.PWNOrder.get(self.pwn_customer_id)

        reconciled_result = pwn_order.reconciled_results

        for r in pwn_order.reconciled_results.results:
            PWNResult.objects.create(
                pwn_order=self,
                clinical_info=reconciled_result.results_summary.clinical_info,
                collection_date=reconciled_result.results_summary.collection_date,
                fasting=none_or_boolean(reconciled_result.results_summary.fasting),
                lab_patient_id=reconciled_result.results_summary.lab_patient_id,
                lab_report_release_date=reconciled_result.results_summary.lab_report_release_date,
                receipt_date=reconciled_result.results_summary.receipt_date,
                reported_date=reconciled_result.results_summary.reported_date,

                result_fasting=r.fasting,
                lab_abnormal_flag=r.lab_abnormal_flag,
                lab_id=r.lab_id,
                lab_reference_range=r.lab_reference_range,
                observation_date=r.observation_date,
                order_lab_code=r.order_lab_code,
                order_lab_name=r.order_lab_name,
                result_lab_code=r.result_lab_code,
                result_lab_name=r.result_lab_name,
                result_status=r.result_status,
                units_of_measurement=r.units_of_measurement,
                value=r.value,
                value_type=r.value_type,
                notes=r.notes,
                lab_facility=r.lab_facility,
                lab_facility_director=r.lab_facility_director,
            )

    def fetch_results(self):
        order_with_results = api.get_customer(self.pwn_customer_id)

        r = order_with_results.find('customer').find('reconciled_results').find('result')
        summary = order_with_results.find('customer').find('reconciled_results').find('results-summary')
        if summary:
            PWNResult.objects.create(
                pwn_order=self,
                clinical_info=summary.find('clinical-info').text if summary and summary.find('clinical-info') else None,
                collection_date=convert_datetime(summary.find('observation-date').text),  # collection_date,
                fasting=none_or_boolean(summary.find('fasting').text.find('text').text),
                lab_patient_id=summary.find('lab-patient-id').text,
                lab_report_release_date=convert_datetime(summary.find('lab-report-release-date').text),  # lab_report_release_date,
                receipt_date=convert_datetime(summary.find('receipt-date').text),  # receipt_date,
                reported_date=convert_datetime(summary.find('reported-date').text),  # reported_date,
                result_fasting=none_or_boolean(r.find('fasting').text if r.find('fasting') else None),
                lab_abnormal_flag=r.find('lab-abnormal-flag').text,
                lab_id=int(r.find('lab-id').text.find('text').text) if r.find('lab-id').text.find('text').text else None,
                lab_reference_range=r.find('lab-reference-range').text,
                observation_date=convert_datetime(summary.find('observation-date').text),  # observation_date,
                order_lab_code=r.find('order-lab-code').text,
                order_lab_name=r.find('order-lab-name').text,
                result_lab_code=r.find('result-lab-code').text,
                result_lab_name=r.find('result-lab-name').text,
                result_status=r.find('result-status').text,
                units_of_measurement=r.find('units-of-measurement').text,
                value=r.find('value').text,
                value_type=r.find('value-type').text,
                notes=r.find('notes').text.find('text').text,
                lab_facility=r.find('lab-facility').text,
                lab_facility_director=r.find('lab-facility-director').text
            )
            return self.results.all()
        else:
            return PWNResult.objects.none()

    
    def from_bs_object(self, bs_info_object):
        """
            Populate self field with info fetched from PWN API
        """
        tag_names = CUSTOMER_TAG_NAMES
        for tag_name in tag_names:
            setattr(self, tag_name, bs_info_object.find(tag_name).text)
        self.zip_code = bs_info_object.find('zip').text
        
        return self

    @classmethod
    def create_for_cusotmer(cls, customer_id):
        """
            Fetch customer information from PWN side
            create an PWNOrder instance from this info
            save it to DB for further usage
        """
        customer = api.get_customer(customer_id=customer_id)
        try:
            pwn_order = cls.objects.get(pwn_customer_id=customer_id)
        except PWNOrder.DoesNotExist:
            pwn_order = PWNOrder(pwn_customer_id=customer_id)

        pwn_order = pwn_order.from_bs_object(bs_info_object=customer)
        pwn_order.save()
        return pwn_order

    def has_results(self):
        if self.reconciled_results:
            return True
        else:
            return False

class PWNResult(models.Model):
    pwn_order = models.ForeignKey(PWNOrder, related_name='results')
    clinical_info = models.CharField(
        max_length=62, null=True, blank=True, help_text=u'Contains the clinical info if such info was sent with the order'
    )
    collection_date = models.DateTimeField(null=True)
    fasting = models.NullBooleanField()
    lab_patient_id = models.CharField(null=True, max_length=255)
    lab_report_release_date = models.DateTimeField(null=True)
    receipt_date = models.DateTimeField(null=True)
    reported_date = models.DateTimeField(null=True)
    #TODO store the linke to the pdf result file
    # results_pdf = models.
    result_fasting = models.NullBooleanField()
    lab_abnormal_flag = models.CharField(null=True, max_length=1)
    lab_id = models.IntegerField(null=True)
    lab_reference_range = models.CharField(null=True, max_length=255)
    observation_date = models.DateTimeField(null=True)
    order_lab_code = models.CharField(null=True, max_length=255)
    order_lab_name = models.CharField(null=True, max_length=255)
    result_lab_code = models.CharField(null=True, max_length=255)
    result_lab_name = models.CharField(null=True, max_length=255)
    result_status = models.CharField(null=True, max_length=1)
    units_of_measurement = models.CharField(null=True, max_length=255)
    value = models.CharField(null=True, max_length=255)
    value_type = models.CharField(null=True, max_length=2)
    notes = models.CharField(null=True, max_length=1000, help_text=u'Holds the comments associated with test result')
    lab_facility = models.CharField(null=True, max_length=255, help_text=u'Laboratory info')
    lab_facility_director = models.CharField(null=True, max_length=255, help_text=u'Laboratory medical director')

    def __str__(self):
        return _("Result #%s for PWN order #%s") % (
            self.pk, self.pwn_order.pk)
