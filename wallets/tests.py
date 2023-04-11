from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from wallets.views import MAX_WALLETS_COUNT


class WalletTests(APITestCase):
    username = "TestUser"
    email = "test@mail.ru"
    password = "TestPassword123"

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(cls.username, cls.email, cls.password)
        cls.token, _ = Token.objects.get_or_create(user=cls.user)

    def test_create_wallet(self):
        """
        Test user can create a wallet.
        """
        self.client.force_authenticate(user=self.user, token=self.token)
        url = reverse("wallet-list")
        data = {"type": "Visa", "currency": "USD"}
        expected_fields = (
            "id",
            "name",
            "type",
            "currency",
            "balance",
            "created_on",
            "modified_on",
            "owner",
        )
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTupleEqual(expected_fields, tuple(response.data.keys()))

    def test_create_max_wallets_for_user(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        url = reverse("wallet-list")
        data = {"type": "Mastercard", "currency": "EUR"}
        for count in range(5):
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0], f"You can't create more then {MAX_WALLETS_COUNT} wallets"
        )

    def test_get_bonus_when_create_a_wallet(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        url = reverse("wallet-list")
        data_usd = {"type": "Visa", "currency": "USD"}
        data_eur = {"type": "Visa", "currency": "EUR"}
        data_rub = {"type": "Visa", "currency": "RUB"}
        response = self.client.post(url, data_usd, format="json")
        self.assertEqual(response.data["balance"], "3.00")
        response = self.client.post(url, data_eur, format="json")
        self.assertEqual(response.data["balance"], "3.00")
        response = self.client.post(url, data_rub, format="json")
        self.assertEqual(response.data["balance"], "100.00")
