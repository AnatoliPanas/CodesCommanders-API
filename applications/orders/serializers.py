from rest_framework import serializers

from applications.orders.models.order import Order


class OrderListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'title',
            'description',
            'status',
            'owner'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'title',
            'description',
            'status',
        ]
        extra_kwargs = {'status': {'required': False}, }


class OrderDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'title',
            'description',
            'status',
            'created_at',
            'owner'
        ]
