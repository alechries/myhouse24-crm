from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='cabinet_index'),
    path('login', views.login_view, name='cabinet_login'),
    path('logout', views.logout_view, name='cabinet_logout'),
    path('statistic', views.statistic_view, name='cabinet_statistic'),
    path('invoice/<int:pk>', views.invoice_view, name='cabinet_invoice'),
    path('invoice/view', views.invoice_view_view, name='cabinet_invoice-view'),
    path('tariffs', views.tariffs_view, name='cabinet_tariffs'),
    path('tariffs/view', views.tariffs_view_view, name='cabinet_tariffs-view'),
    path('messages', views.messages_index, name='cabinet_messages'),
    path('messages/view', views.messages_view, name='cabinet_messages-view'),
    path('messages/create', views.messages_create_view, name='cabinet_messages-create'),
    path('messages/delete', views.messages_delete_view, name='cabinet_messages-delete'),
    path('master-request', views.master_request_view, name='cabinet_master-request'),
    path('master-request/create', views.master_request_create_view, name='cabinet_master-request-create'),
    path('master-request/delete/<int:pk>', views.master_request_delete_view, name='cabinet_master-request-delete'),
    path('user', views.user_view, name='cabinet_user'),
    path('user/change', views.user_change_view, name='cabinet_user-change'),
]