from rest_framework import serializers

from .models import Provider, Currency, Pair, Trade


class BlotterTradesSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    pair = serializers.SerializerMethodField()

    class Meta:
        model = Trade
        fields = ("id", "date", "pair", "price", "quantity")

    def get_date(self, obj):
        return {
            "date": obj.date.strftime("%Y/%m/%d"),
            "time": obj.date.strftime("%H:%M:%S.%f")[:-3],
        }

    def get_pair(self, obj):
        return {"id": obj.pair.id, "acronyms": obj.pair.joined_acronyms}


class BlotterTradesGraphSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Trade
        fields = ("id", "date", "price")

    def get_date(self, obj):
        return {
            "date": obj["date"].strftime("%Y/%m/%d"),
            "time": obj["date"].strftime("%H:%M:%S.%f")[:-3],
        }


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ("pk", "provider", "pair", "quantity", "price")

    def create(self, validated_data):
        user = self.context["request"].user

        data = {
            "trader": user,
            "provider": validated_data["provider"],
            "pair": validated_data["pair"],
            "quantity": validated_data["quantity"],
            "price": validated_data["price"],
        }

        return Trade.objects.create(**data)


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ("id", "name", "acronym")


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "name", "acronym")


class PairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pair
        fields = ("id", "from_currency", "to_currency")