from rest_framework import status
from django.core.cache import cache
from django.test import TestCase, Client
from django.conf import settings

User = settings.AUTH_USER_MODEL


class TestSendOTP(TestCase):

    def setUp(self):
        self.client = Client()

    def make_post_request(self, data):
        return self.client.post(f'/api/v1/customers/send_otp/', data)

    def test_if_data_is_invalid_returns_400(self):
        data = {}

        response = self.make_post_request(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_data_is_valid_returns_201(self):
        data = {'phone_number': '09123456789'}

        response = self.make_post_request(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestVerify(TestCase):

    def setUp(self):
        self.client = Client()
        self.phone_number = '09123456789'
        self.code = 123456
        cache.set(key=self.phone_number, value=self.code, timeout=2 * 60)

    def make_post_request(self, data):
        return self.client.post(f'/api/v1/customers/verify/', data)

    def test_if_data_is_invalid_returns_400(self):
        data = {}

        response = self.make_post_request(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_data_is_valid_returns_201(self):
        data = {'phone_number': self.phone_number, 'code': self.code}

        response = self.make_post_request(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
