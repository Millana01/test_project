from rest_framework import serializers

from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Wallet
        fields = [
            "id",
            "name",
            "type",
            "currency",
            "balance",
            "created_on",
            "modified_on",
            "owner",
        ]
