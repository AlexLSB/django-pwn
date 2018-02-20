# -*- coding: utf-8 -*-
from bs4 import NavigableString
import dateutil.parser

from api import PWNAPIResource


api = PWNAPIResource()


RESULT_TAG_NAMES = [
    "customer-id", "id", "lab-abnormal-flag", "lab-facility-director-id", "fasting",
    "lab-facility-id", "lab-id", "lab-reference-range", "obx-sequence-number", "order-lab-code",
    "order-lab-name", "result-lab-code", "result-lab-name", "result-status", "tnp-reason",
    "hl7message-nte-id", "observation-date",
    "units-of-measurement", "value", "value-type", "notes", "lab-facility", "lab-facility-director"]


class Group(object):
    @staticmethod
    def from_lxml(document):
        instance = Group()
        instance.id = document.xpath('.//id/text()')[0]
        instance.name = document.xpath('.//name/text()')[0]
        instance.lab_id = document.xpath('.//lab_id/text()')[0]
        try:
            account_number = document.xpath('.//account_number/text()')[0]
        except IndexError:
            account_number = None
        instance.account_number = account_number
        instance.tests = [PWNTest.from_lxml(tag) for tag in document.xpath('.//test_types/*')]
        return instance

    @staticmethod
    def filter(**kwargs):
        document = api.test_groups(**kwargs)
        return [Group.from_lxml(tag) for tag in document.xpath('//test_groups/*')]


class TestDisclimer(object):
    @staticmethod
    def from_lxml(document):
        instance = TestDisclimer()
        instance.id = document.xpath('.//id/text()')[0]
        instance.value = document.xpath('.//disclaimer/text()')[0]
        return instance


class PWNTest(object):
    @staticmethod
    def from_lxml(document):
        instance = PWNTest()
        instance.name = document.xpath('.//name/text()')[0]
        try:
            lab_code = document.xpath('.//lab_code/text()')[0]
        except:
            lab_code = None
        instance.lab_code = lab_code
        instance.code = document.xpath('.//code/text()')[0]
        instance.same_day = True if document.xpath('.//same_day/text()')[0] == 'true' else False
        instance.disclaimers_required = True if document.xpath('.//disclaimers_required/text()')[0] == 'true' else False
        instance.required_gender = document.xpath('.//required_gender/text()')[0]
        instance.customer_physician_required = True if document.xpath('.//customer_physician_required/text()')[0] == 'true' else False
        instance.fasting_required = True if document.xpath('.//fasting_required/text()')[0] == 'true' else False
        instance.disclaimers = [TestDisclimer.from_lxml(tag) for tag in document.xpath('.//test_disclaimers/*')]
        return instance

    @staticmethod
    def filter(laboratory=None):
        if laboratory:
            document = api.test_types(laboratory.lab_id)
        else:
            document = api.test_types()
        return [PWNTest.from_lxml(tag) for tag in document.xpath('//test_types/*')]

    def __unicode__(self):
        return ' '.join([self.name, self.code])


class ResultSummary(object):
    @staticmethod
    def from_xml(document):
        instance = ResultSummary()
        try:
            instance.clinical_info = document.xpath('.//clinical-info/text()')[0]
        except IndexError:
            instance.clinical_info = None
        try:
            instance.collection_date = dateutil.parser.parse(document.xpath('.//collection-date/text()')[0])
        except IndexError:
            instance.collection_date = None
        try:
            instance.fasting = True if document.xpath('.//fasting/text()')[0] == 'true' else False
        except IndexError:
            instance.fasting = None
        try:
            instance.lab_patient_id = document.xpath('.//lab-patient-id/text()')[0]
        except IndexError:
            instance.lab_patient_id = None
        try:
            instance.lab_report_release_date = dateutil.parser.parse(document.xpath('.//lab-report-release-date/text()')[0])
        except IndexError:
            instance.lab_report_release_date = None
        try:
            instance.receipt_date = dateutil.parser.parse(document.xpath('.//receipt-date/text()')[0])
        except:
            instance.receipt_date = None
        try:
            instance.reported_date = dateutil.parser.parse(document.xpath('.//reported-date/text()')[0])
        except:
            instance.reported_date = None
        return instance


class Result(object):

    @classmethod
    def from_xml(cls, xml):
        tag_names = RESULT_TAG_NAMES
        instance = cls()
        for tag_name in tag_names:
            setattr(instance, tag_name.replace("-", "_"), xml.find(tag_name).text)
        instance.fasting = True if instance.fasting == "true" else False
        instance.hl7message_nte_id = instance.hl7message_nte_id or None
        instance.observation_date = dateutil.parser.parse(instance.observation_date)
        return instance


class RecognizedResult(object):
    @staticmethod
    def from_xml(document):
        instance = RecognizedResult()
        try:
            instance.pdf = document.xpath('.//results-pdf/text()')[0]
        except:
            instance.pdf = None
        instance.results_summary = ResultSummary.from_xml(document.xpath('.//results-summary')[0])
        instance.results = list()
        for result_tag in document.xpath('.//result'):
            instance.results.append(Result.from_xml(result_tag))

        return instance


class PWNLab(object):
    """
        Reflects Resellers Laboratory from PWN
    """

    def __init__(self, id, lab_id, account, user_id):
        self.id = id
        self.lab_id = lab_id
        self.account = account
        self.user_id = user_id

    def __repr__(self):
        return u"<PWNLab: #%s account: %s>" % (self.id, self.account)

    @staticmethod
    def all():
        document = api.registered_labs()
        laboratory_tags = document.xpath('//reseller-labs/*')
        return [Laboratory.from_lxml(tag) for tag in laboratory_tags]

    @property
    def groups(self):
        return Group.filter(lab_id=self.lab_id)

    @property
    def tests(self):
        document = api.test_types()
        return [PWNTest.from_lxml(tag) for tag in document.xpath('//test_types/*')]

class PWNClient(object):
    """
        Client to request labs list and etc
    """

    def get_labs(self):
        """
            Return list of reseller labs
        """
        labs_data = api.registered_labs()
        labs = labs_data.find_all('reseller-lab')
        lab_objs = []
        for lab in labs:
            lab_objs.append(
                PWNLab(
                    id=lab.find('id').text,
                    lab_id=lab.find('lab-id').text,
                    account=lab.find('account').text,
                    user_id=lab.find('user-id').text,
                ))
        return lab_objs

    def get_orders(self):
        """
            Return all orders in PWN
        """
        return self.get_customers()

    def get_customers(self):
        """
            Return all orders in PWN
        """
        customers = api.customers()
        customers_list = []
        for customer in customers.find_all('customer'):
            customer_dict = {tag.name: tag.text for tag in customer if not isinstance(tag, NavigableString)}
            customers_list.append(customer_dict)
        return customers_list
