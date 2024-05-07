from django.urls import path
from . import views
urlpatterns = [ 
    # ============AUTH============
    path('finance_login/',views.finance_login,name='finance_login'),
    path('finance_logout/',views.finance_logout,name='finance_logout'),
    # ============

    path('finance_dahboard/',views.finance_dahboard,name='finance_dahboard'),
]