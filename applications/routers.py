from django.urls import path

from applications.orders.views import OrderListCreateGenericAPIView, OrderDetailUpdateDeleteGenericAPIView
from applications.users.views import (RegisterUserAPIView,
                                      LogInAPIView,
                                      LogOutAPIView)

urlpatterns = [
    path('auth-register/', RegisterUserAPIView.as_view()),
    path('auth-login/', LogInAPIView.as_view()),
    path('auth-logout/', LogOutAPIView.as_view()),

    path('order/', OrderListCreateGenericAPIView.as_view()),
    path('order/<int:order_id>/', OrderDetailUpdateDeleteGenericAPIView.as_view()),
]
