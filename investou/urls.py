from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('master.urls')),
    path('debug/',include('debug.urls')),
    path('authentication/',include('authentication.urls')),
    path('client/',include('client.urls')),
    path('staff/',include('staff.urls')),
    path('finance/',include('finance.urls')),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)