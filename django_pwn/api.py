# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import datetime
import requests
from dicttoxml import dicttoxml
import xmltodict

from .exceptions import PWNAPIError
from .settings import pwn_settings


CUSTOMER_STATUS_ALL = 'all'
CUSTOMER_STATUS_PENDING = 'pending'
CUSTOMER_STATUS_APPROVED = 'approved'
CUSTOMER_STATUS_REJECTED = 'rejected'
CUSTOMER_STATUS_RESULTS = 'results'

CONTACT_TYPES_CALL = 'CallLog'
CONTACT_TYPES_LETTER = 'LetterLog'
CONTACT_TYPES_EMAIL = 'EmailLog'

GENDER_MALE = 'Male'
GENDER_FEMALE = 'Female'


class PWNAPIResource(object):
    def __init__(self):
        self.pwn_host = pwn_settings.PWN_HOST
        self.auth = (pwn_settings.API_KEY, pwn_settings.API_TOKEN)

    @staticmethod
    def get(url, auth, params=None, headers=None):
        """
            Makes a get request to the PWN API
        """
        return requests.get(url, auth=auth, params=params, headers=headers).text.replace(' encoding="UTF-8"', '')

    @staticmethod
    def post(url, auth, data=None, headers=None):
        """
            Make a post request to the PWN API
        """
        return requests.post(url, data=data, auth=auth, headers=headers).text.replace(' encoding="UTF-8"', '')

    def request_api(self, path, params=None, post_data=None, as_dict=False):
        """
            Make a request to the PWN API (post or get depends on data)
        """
        url = self.pwn_host + path
        if post_data:
            headers = {'Content-type': 'application/xml'}
            xml_string = PWNAPIResource.post(url, auth=self.auth, data=post_data, headers=headers)
        else:
            xml_string = PWNAPIResource.get(url, auth=self.auth, params=params)
        if as_dict:
            return xmltodict.parse(xml_string)
        try:
            result_soup = BeautifulSoup(xml_string, 'xml')
        except Exception, e:
            raise PWNAPIError("Error parsing PWN Result! %s" % e)
        else:
            if result_soup.find().name == 'errors':
                raise PWNAPIError("PWN API Error: %s" % xml_string)
        return result_soup

    def test_types(self, lab_id=None):
        path = 'test_types'
        params = {'lab_id': lab_id} if lab_id else {}
        return self.request_api(path, params=params)

    def test_groups(self, lab_id=None, account_number=None, name=None):
        params = {
            'lab_id': lab_id,
            'account_number': account_number,
            'name': name
        }
        return self.request_api('test_groups', params=params)

    def customers(self, status=CUSTOMER_STATUS_ALL, start_date=datetime.date(1971, 1, 1),
                  end_date=datetime.date.today(), page=1, per_page=1000):
        params = {
            'status': status,
            'start_date': start_date.strftime('%Y%m%d'),
            'end_date': end_date.strftime('%Y%m%d'),
            'page': page,
            'per_page': per_page
        }
        return self.request_api('customers', params=params)

    def create_customer(self,
                        first_name,
                        last_name,
                        gender,
                        dob,
                        state,
                        zip_code,
                        city,
                        test_types,
                        take_tests_same_day,
                        email,
                        address,
                        work_phone):
        """
            Create a PWN Order for a customer with given fields
        """
        request_dict = {
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "dob": dob,
            "state": state,
            "zip": zip_code,
            "city": city,
            "test_types": test_types,
            "take_tests_same_day": take_tests_same_day,
            "email": email,
            "address": address,
            "work_phone": work_phone,
        }
        data = dicttoxml(request_dict, custom_root='customer')
        result = self.request_api('customers', post_data=data)
        return result

    def get_customer(self, customer_id):
        """
            Get Order info from PWN with results.
            Used to fetch the results.
        """
        path = 'customers/{}'.format(customer_id)
        xml_dict = self.request_api(path, params={'include': 'reconciled_results'})
        # xml_dict['customer']['zip_code'] = xml_dict['customer'].pop('zip')
        return xml_dict

    def registered_labs(self):
        return self.request_api('registered_labs')

    def result_test_types(self):
        return self.request_api('result_test_types')

    def set_customer_contact_log(self, customer_id, type, notes):
        data = dicttoxml({'type': type, 'notes': notes}, custom_root='contact_log')
        path = 'customers/{}/contact_logs.xml'.format(customer_id)
        return self.request_api(path, post_data=data)

    def get_customer_contact_log(self, customer_id):
        path = 'customers/{}/contact_logs.xml'.format(customer_id)
        return self.request_api(path)

    def find_psc(self, zipcode):
        path = 'find_psc/{}'.format(str(zipcode))
        return self.request_api(path)
