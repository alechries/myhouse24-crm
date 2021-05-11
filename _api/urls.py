from django.urls import path
from . import views

urlpatterns = [
    path('house/', views.HouseList.as_view(), name='api-house-list'),
    path('house/<int:pk>', views.HouseDetail.as_view(), name='api-house-detail'),
]

