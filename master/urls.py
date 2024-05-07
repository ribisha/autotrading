from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('news/',views.news,name='news'),


    #===================STAFF_MANAGEMENT#===================
    
    path('master_staff_add/',views.master_staff_add,name='master_staff_add'),
    path('all_staff',views.all_staff,name='all_staff'),
    path('staff_profile_management/<str:sk>/',views.staff_profile_management,name='staff_profile_management'),
    path('m_staff_delete_user/<int:staff_user_id>/',views.m_staff_delete_user, name='m_staff_delete_user'),
    #===================END_STAFF_MANAGEMENT#===================


    #===================CLIENT_MANAGEMENT#===================
    path('master_client_add/',views.master_client_add,name='master_client_add'),
    path('all_accepted_client/',views.all_accepted_client,name='all_accepted_client'),
    # path('all_client/',views.all_client,name='all_client'),
    path('client_profile_management/<str:pk>/',views.client_profile_management,name='client_profile_management'),
    path('m_client_delete_user/<int:user_id>/',views.m_client_delete_user, name='m_client_delete_user'),
    path('connected_users/', views.display_connected_users, name='display_connected_users'),
    path('connect_now/', views.connect_now, name='connect_now'),
    
    # path('connectapi_detail/<int:connectapi_id>/', views.connectapi_detail, name='connectapi_detail'),
    #===================END_CLIENT_MANAGEMENT#===================

    #===================FINANCE_MANAGEMENT#===================
    path('master_finance_add/',views.master_finance_add,name='master_finance_add'),
    path('all_finance/',views.all_finance,name='all_finance'),
    path('my_account_master/',views.my_account_master,name='my_account_master'),
    path('master_open_account/',views.master_open_account,name='master_open_account'),
    path('master_create_courses/',views.master_create_courses,name='master_create_courses'),
    path('master_finance_user_delete/<int:finance_user_id>/',views.master_finance_user_delete,name='master_finance_user_delete'),
    # #===================END_FINANCE_MANAGEMENT===================

    # ====================MASTER_AUTH#===================
    path('master_register/',views.master_register,name='master_register'),
    path('master_login/',views.master_login,name='master_login'),
    path('master_logout/',views.master_logout, name='master_logout'),
    path('m_select_broker/', views.m_select_broker, name='m_select_broker'),
    path('master/m_connect_api/<str:m_broker>/', views.m_connect_api, name='m_connect_api'), 
    path('m_fetched_data/', views.m_fetched_datas, name='m_fetched_data'),
    path('place_trade_order/', views.place_trade_order, name='place_trade_order'),
    path('create_room/', views.create_room, name='create_room'),
    path('all_room/', views.all_room, name='all_room'),
    path('accept_reject/', views.accept_reject, name='accept_reject'),
    # path('test/',views.test,name='test'),

    # ====================END-MASTER_AUTH====================

    # ==========================STOCK_MARKET_DATA==========================
    path('index_5_stock/',views.index_5_stock,name='index_5_stock'),
    path('index_top50_stock/',views.index_top50_stock,name='index_top50_stock'),
    path('index_master_suggested_stock/',views.index_master_suggested_stock,name='index_master_suggested_stock'),
]