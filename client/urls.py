from django.urls import path
from . import views
urlpatterns = [ 
    # ------------------AUTH------------------
    path('client_login/',views.client_login,name='client_login'),
    path('client_register/',views.client_register,name='client_register'),
    path('select_broker/', views.select_broker, name='select_broker'),
    path('client/connect_api/<str:broker>/', views.connect_api, name='connect_api'),
    path('fetched_data/', views.fetched_datas, name='fetched_data'),
    # path('place_trade_order/', views.place_trade_order, name='place_trade_order'),
    path('all_client/', views.all_client, name='all_client'),
   
    path('client_logout/',views.client_logout,name='client_logout'),
    path('client_open_account/',views.client_open_account,name='client_open_account'),

    path('client_dashboard/',views.client_dashboard,name='client_dashboard'),
    path('c_courses/',views.c_courses,name='c_courses'),

    path('c_profile/',views.c_profile,name='c_profile'),
    path('client_news/',views.client_news,name='client_news'),

    # ==========================STOCK_MARKET_DATA==========================
    path('client_index_5_stock/', views.client_index_5_stock, name='client_index_5_stock'),
    path('client_index_top50_stock/',views.client_index_top50_stock,name='client_index_top50_stock'),
    path('client_index_master_suggested_stock/',views.client_index_master_suggested_stock,name='client_index_master_suggested_stock'),
]