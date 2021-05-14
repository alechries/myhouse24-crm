from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='public_index'),
    path('about', views.about_view, name='public_about'),
    path('services', views.services_view, name='public_services'),
    path('contact', views.contact_view, name='public_contact'),
    path('about', views.about_view, name='public_about'),
    path('error', views.error_view, name='public_error'),
]

