from typing import Any

from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from wallets.models import Wallet
from wallets.serializers import WalletSerializer

MAX_WALLETS_COUNT = 5


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "name"
    lookup_url_kwarg = "name"

    def validate_wallet_before_create(
        self, request: Request, serializer: WalletSerializer
    ) -> None:
        wallets_count = Wallet.objects.filter(owner=request.user).count()
        if wallets_count == MAX_WALLETS_COUNT:
            raise ValidationError(
                detail=f"You can't create more then {MAX_WALLETS_COUNT} wallets"
            )
        if request.data["currency"] == "USD" or "EUR":
            serializer.validated_data["balance"] = 3.00
        if request.data["currency"] == "RUB":
            serializer.validated_data["balance"] = 100.00

    def perform_create(self, serializer: WalletSerializer):
        serializer.save(owner=self.request.user)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate_wallet_before_create(request, serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
