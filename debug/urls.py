from django.urls import path
from . import views

urlpatterns = [
    path('newss/',views.news,name='newss'),
    path('news_details/',views.news_details,name='news_details'),
    path('redirect_to_original/<path:article_url>/', views.redirect_to_original, name='redirect_to_original'),
    path('news_a/',views.news_a,name='news_a'),
    path('news_b/',views.news_b,name='news_b')
]