from django.urls import path, include
import noter
from .views import *

app_name = 'noter'

urlpatterns = [
    path('/home/<str:name>/', show_all, name="home"), 
    path('add/<str:name>', add_note, name='add' ),
    path('fav_delete/<str:name>', fav_delete, name='fav_delete')
]
