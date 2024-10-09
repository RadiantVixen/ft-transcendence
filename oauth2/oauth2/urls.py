from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Oapp.urls')),
    path('test/', include('Oapp.test_view'))
]
