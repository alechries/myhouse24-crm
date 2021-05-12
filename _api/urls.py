from django.urls import path
from . import views


urlpatterns = [
    path('house/', views.HouseList.as_view(), name='api-house-list'),
    path('house/<int:pk>', views.HouseDetail.as_view(), name='api-section-detail'),
    path('section/', views.SectionList.as_view(), name='api-section-list'),
    path('section/<int:pk>', views.SectionDetail.as_view(), name='api-section-detail'),
]

