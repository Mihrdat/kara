from rest_framework import status
from django.core.cache import cache
from django.test import TestCase
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class TestCustomerViews(TestCase):
    def test_if_data_is_invalid_send_otp_returns_400(self):
        data = {}
        url = reverse("customer-send-otp")

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_data_is_valid_send_otp_returns_200(self):
        data = {"phone_number": "09123456789"}
        url = reverse("customer-send-otp")

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_data_is_invalid_verify_returns_400(self):
        data = {}
        url = reverse("customer-verify")

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_data_is_valid_verify_returns_200_or_201(self):
        phone_number = "09123456789"
        code = "123456"
        cache.set(key=phone_number, value=code, timeout=2 * 60)
        data = {"phone_number": phone_number, "code": code}
        url = reverse("customer-verify")

        response = self.client.post(url, data)

        self.assertIn(
            response.status_code, (status.HTTP_200_OK, status.HTTP_201_CREATED)
        )
