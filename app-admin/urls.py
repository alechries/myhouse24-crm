from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='admin_index'),
    path('update-me', views.update_me_view, name='admin_update-me'),
    path('login', views.login_view, name='admin_login'),
    path('logout', views.logout_view, name='admin_logout'),
    path('account-transaction', views.account_transaction_view, name='admin_account-transaction'),
    path('accont-transaction/<int:pk>', views.account_transaction_detail_view, name='admin_account-transaction-detail'),
    path('account-transaction/create-in', views.account_transaction_create_in_view, name='admin_account-transaction-create_in'),
    path('account-transaction/create-out', views.account_transaction_create_out_view, name='admin_account-transaction-create_out'),
    path('account-transaction/change/<int:pk>', views.account_transaction_change_view, name='admin_account-transaction-change'),
    path('account-transaction/delete/<int:pk>', views.account_transaction_delete_view, name='admin_account-transaction-delete'),
    path('invoice', views.invoice_view, name='admin_invoice'),
    path('invoice/create', views.invoice_create_view, name='admin_invoice-create'),
    path('invoice/copy', views.invoice_copy_view, name='admin_invoice-copy'),
    path('invoice/change', views.invoice_change_view, name='admin_invoice-change'),
    path('invoice/delete', views.invoice_delete_view, name='admin_invoice-delete'),
    path('account', views.account_view, name='admin_account'),
    path('account/detail/<int:pk>', views.account_detail, name='admin_account-detail'),
    path('account/create', views.account_create_view, name='admin_account-create'),
    path('account/change/<int:pk>', views.account_change_view, name='admin_account-change'),
    path('account/delete/<int:pk>', views.account_delete_view, name='admin_account-delete'),
    path('apartment', views.apartment_view, name='admin_apart'),
    path('apartment/detail/<int:pk>', views.apartment_detail_view, name='admin_apart-detail'),
    path('apartment/create', views.apartment_create_view, name='admin_apart-create'),
    path('apartment/change/<int:pk>', views.apartment_change_view, name='admin_apart-change'),
    path('apartment/delete/<int:pk>', views.apartment_delete_view, name='admin_apart-delete'),
    path('user', views.user_view, name='admin_user'),
    path('user/detail/<int:pk>', views.user_detail_view, name='admin_user-detail'),
    path('user/create', views.user_create_view, name='admin_user-create'),
    path('user/change/<int:pk>', views.user_change_view, name='admin_user-change'),
    path('user/delete/<int:pk>', views.user_delete_view, name='admin_user-delete'),
    path('house', views.house_view, name='admin_house'),
    path('house/create', views.house_create_view, name='admin_house-create'),
    path('house/change/<int:pk>', views.house_change_view, name='admin_house-change'),
    path('house/delete/<int:pk>', views.house_delete_view, name='admin_house-delete'),
    path('message', views.message_view, name='admin_message'),
    path('message/create', views.message_create_view, name='admin_message-create'),
    path('message/detail/<int:pk>', views.message_detail_view, name='admin_message-detail'),
    path('message/delete/<int:pk>', views.message_delete_view, name='admin_message-delete'),
    path('master-request', views.master_request_view, name='admin_master-request'),
    path('master-request/create', views.master_request_create_view, name='admin_master-request-create'),
    path('master-request/change/<int:pk>', views.master_request_change_view, name='admin_master-request-change'),
    path('master-request/delete/<int:pk>', views.master_request_delete_view, name='admin_master-request-delete'),
    path('counters', views.counters_view, name='admin_counters-view'),
    path('counter/apartment/<int:pk>', views.counter_house_view, name='admin_counter-house-view'),
    path('meter-data/create', views.meter_data_create_view, name='admin_meter-data-create'),
    path('meter-data/detail/<int:pk>', views.meter_data_detail_view, name='admin_meter-data-detail'),
    path('meter-data/change/<int:pk>', views.meter_data_change_view, name='admin_meter-data-change'),
    path('meter-data/delete/<int:pk>', views.meter_data_delete_view, name='admin_meter-data-delete'),
    path('website/main-page', views.website_main_page_view, name='admin_website-main-page'),
    path('website/about', views.website_about_view, name='admin_website-about'),
    path('website/about/gallery/delete/<int:pk>', views.website_about_gallery_delete_view, name='admin_website-about-gallery-delete'),
    path('website/services', views.website_services_view, name='admin_website-services'),
    path('website/services/blocks/delete/<int:pk>', views.website_services_blocks_delete_view, name='admin_website-services-blocks-delete'),
    path('website/tariffs', views.website_tariffs_view, name='admin_website-tariffs'),
    path('website/tariffs/blocks/delete/<int:pk>', views.website_tariffs_blocks_delete_view, name='admin_website-tariffs-blocks-delete'),
    path('website/contact', views.website_contact_view, name='admin_website-contact'),
    path('services', views.services_view, name='admin_services'),
    path('tariffs', views.tariffs_view, name='admin_tariffs'),
    path('tariffs/create', views.tariffs_change_view, name='admin_tariffs-create'),
    path('tariffs/change/<int:pk>', views.tariffs_change_view, name='admin_tariffs-change'),
    path('tariffs/copy', views.tariffs_copy_view, name='admin_tariffs-copy'),
    path('tariffs/delete/<int:pk>', views.tariffs_delete_view, name='admin_tariffs-delete'),
    path('user-app-admin/role', views.user_admin_role_view, name='admin_user-admin-role'),
    path('user-app-admin/users/list', views.user_admin_users_list, name='admin_user-users-list'),
    path('user-app-admin/create', views.user_admin_create_view, name='admin_user-admin-create'),
    path('user-app-admin/change/<int:pk>', views.user_admin_change_view, name='admin_user-admin-change'),
    path('user-app-admin/delete', views.user_admin_delete_view, name='admin_user-admin-delete'),
    path('pay-company', views.pay_company_view, name='admin_pay-company'),
    path('transaction-purpose', views.transaction_purpose_view, name='admin_transaction-purpose'),
    path('transaction-purpose/create', views.transaction_purpose_create_view, name='admin_transaction-purpose-create'),
    path('transaction-purpose/change/<int:pk>', views.transaction_purpose_change_view, name='admin_transaction-purpose-change'),
    path('transaction-purpose/delete/<int:pk>', views.transaction_purpose_delete_view, name='admin_transaction-purpose-delete'),
]