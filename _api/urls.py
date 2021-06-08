from django.urls import path
from . import views


urlpatterns = [
    path('house/', views.HouseList.as_view(), name='house-list'),
    path('house/<int:pk>', views.HouseDetail.as_view(), name='house-detail'),
    path('section/', views.SectionList.as_view(), name='section-list'),
    path('section/<int:pk>', views.SectionDetail.as_view(), name='section-detail'),
    path('floor/', views.FloorList.as_view(), name='floor-list'),
    path('floor/<int:pk>', views.FloorDetail.as_view(), name='floor-detail'),
    path('apartment/', views.ApartmentList.as_view(), name='apartment-list'),
    path('apartment/<int:pk>', views.ApartmentDetail.as_view(), name='apartment-detail'),
    path('service/', views.ServiceList.as_view(), name='service-list'),
    path('service/<int:pk>', views.ServiceDetail.as_view(), name='service-detail'),
    path('measure/', views.MeasureList.as_view(), name='measure-list'),
    path('measure/<int:pk>', views.MeasureDetail.as_view(), name='measure-detail'),
    path('tariffservice/', views.TariffServiceList.as_view(), name='tariffservice-list'),
    path('tariffservice/<int:pk>', views.TariffServiceDetail.as_view(), name='tariffservice-detail'),
    path('account/', views.AccountList.as_view(), name='account-list'),
    path('account/<int:pk>', views.AccountDetail.as_view(), name='account-detail'),
    path('user/', views.UserList.as_view(), name='user-list'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('chart/data', views.ChartData.as_view()),
]

