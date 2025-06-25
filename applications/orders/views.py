from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from applications.orders.models.order import Order
from applications.orders.serializers import OrderListSerializer, OrderCreateSerializer, OrderDetailSerializer
from applications.permissions.permissions import IsOwnerOrReadOnly


class OrderListCreateGenericAPIView(ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['title', 'owner__username', 'owner__email']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderListSerializer
        return OrderCreateSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.select_related('owner').filter(owner=user)
        return queryset

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        status = serializer.validated_data.get('status')

        order = Order.objects.filter(
            title=title,
            status=status,
            is_deleted=False
        )

        if order.exists():
            raise PermissionDenied(
                f"Такой заказ уже подавался"
            )

        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Заказ успешно создан',
            'data': response.data
        }, status=status.HTTP_201_CREATED)


class OrderDetailUpdateDeleteGenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    lookup_url_kwarg = 'order_id'

    def get_queryset(self):
        return Order.objects.select_related('owner')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderDetailSerializer
        else:
            return OrderCreateSerializer

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("Заказ не доступен")
        return obj

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
