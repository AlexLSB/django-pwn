# coding: utf-8


from django.test import TestCase

from django_pwn.utils import PWNAPIResource as Pwn, Laboratory, PWNOrder, Group, PWNTest
from django_pwn.api import GENDER_MALE


class APITestCase(TestCase):
    def test_test_types(self):
        api = Pwn()
        document = api.test_types()
        self.assertNotEqual(document.xpath('//test_types'), [])

    def test_test_groups(self):
        api = Pwn()
        document = api.test_groups()
        self.assertNotEqual(document.xpath('//test_groups'), [])

    def test_customers(self):
        api = Pwn()
        document = api.customers()
        self.assertNotEqual(document.xpath('//customers'), [])

    def test_create_customer(self):
        api = Pwn()
        test_types = api.test_types()
        test_codes = ','.join(test_types.xpath('//code/text()'))
        result = api.create_customer(
            first_name='Tester',
            last_name='Test',
            gender=GENDER_MALE,
            dob='19700101',
            state='CA',
            zip_code='90210',
            city='LA',
            test_types=test_codes,
            take_tests_same_day='true',
            email='test@tester.ru',
            address='address',
            work_phone='5555555555'
        )
        self.assertEqual(result.xpath('//first_name/text()')[0], 'Tester')
        self.assertEqual(result.xpath('//last_name/text()')[0], 'Test')
        self.assertEqual(result.xpath('//email/text()')[0], 'test@tester.ru')

    def test_get_customer(self):
        api = Pwn()
        test_types = api.test_types()
        test_codes = ','.join(test_types.xpath('//code/text()'))

        result = api.create_customer(
            first_name='Tester',
            last_name='Test',
            gender=GENDER_MALE,
            dob='19700101',
            state='CA',
            zip_code='90210',
            city='LA',
            test_types=test_codes,
            take_tests_same_day='true',
            email='test@tester.ru',
            address='address',
            work_phone='5555555555'
        )

        customer_id = result.xpath('//id/text()')[0]
        customer = api.get_customer(customer_id)

        self.assertEqual(customer.xpath('//first_name/text()')[0], result.xpath('//first_name/text()')[0])


class ModelTestCase(TestCase):
    def test_laboratory(self):
        laboratories = Laboratory.all()
        self.assertNotEqual(laboratories, [])
        lab = laboratories[0]
        groups = lab.groups
        self.assertNotEqual(groups, [])
        group = groups[0]
        self.assertEqual(lab.lab_id, group.lab_id)

        tests = lab.tests
        self.assertNotEqual(tests, [])

    def test_group(self):
        groups = Group.filter()
        self.assertNotEqual(groups, [])

    def test_pwntest(self):
        tests = PWNTest.filter()
        self.assertNotEqual(tests, [])

    def test_customer(self):
        test = PWNTest.filter()[0]

        c = PWNOrder()
        c.first_name = 'Tester'
        c.last_name = 'Test'
        c.gender = GENDER_MALE
        c.dob = '19700101'
        c.state = 'CA'
        c.zip_code = '90210'
        c.city = 'LA'
        c.test_types = test.code
        c.take_tests_same_day = 'true'
        c.email = 'test@tester.ru'
        c.address = 'address'
        c.work_phone = '5555555555'
        c = PWNOrder.send(c)
        self.assertNotEqual(c.id, None)

    def test_get_customer(self):
        print '+++++++++++++++++++++++++++++++++++++++++++++++++'
        customer = PWNOrder.get('862878')
        print customer.reconciled_results.pdf
        self.assertEqual(customer.id, '862878')
        print '+++++++++++++++++++++++++++++++++++++++++++++++++'
