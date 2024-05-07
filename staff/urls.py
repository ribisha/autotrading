from django.urls import path
from . import views
urlpatterns = [ 
    # ------------AUTH  
    path('staff_register/',views.staff_register,name='staff_register'),
    path('staff_login/',views.staff_login,name='staff_login'),
    path('staff_logout/',views.staff_logout,name='staff_logout'),
    # ------------
    path('staff_dashboard/',views.staff_dashboard,name='staff_dashboard'),
    
    # ----------------ADDCLIENT
    path('staff_add_client/',views.staff_add_client,name='staff_add_client'),
    path('staff_all_client',views.staff_all_client,name='staff_all_client'),
    path('staff_client_delete_user/<int:client_user_id>/',views.staff_client_delete_user,name='staff_client_delete_user'),
    path('staff_client_profile_management/<str:s_c_m>/',views.staff_client_profile_management,name='staff_client_profile_management'),
    path('staff_client_lead_management/',views.staff_client_lead_management,name='staff_client_lead_management'),

    # ----------PROFILE
    path('staff_profile/',views.staff_profile,name='staff_profile'),
    path('staff_open_account/',views.staff_open_account,name='staff_open_account'),
    
    #------------------ANGELONE--------------------------------------------------------
    
    path('s_select_broker/', views.s_select_broker, name='s_select_broker'),
    path('staff/s_connect_api/<str:s_broker>/', views.s_connect_api, name='s_connect_api'), 
    path('s_fetched_data/', views.s_fetched_data, name='s_fetched_data'),
    path('all_clients/', views.all_clients, name='all_clients'),
    path('s_connect_now/', views.s_connect_now, name='s_connect_now'),
    path('s_accepted_client/',views.s_accepted_client,name='s_accepted_client'),
     path('s_place_trade_order/', views.s_place_trade_order, name='s_place_trade_order'),
]