from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('app.urls')),
     path('noter/', include(('noter.urls', 'noter'), namespace='noter')),
]
