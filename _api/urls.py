from django.urls import path
from . import views


urlpatterns = [
    path('house/', views.HouseList.as_view(), name='house-list'),
    path('house/<int:pk>', views.HouseDetail.as_view(), name='house-detail'),
    path('section/', views.SectionList.as_view(), name='section-list'),
    path('section/<int:pk>', views.SectionDetail.as_view(), name='section-detail'),
]

