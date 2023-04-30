from django.urls import path,include
from .views import *


urlpatterns = [
    path('',login),  
    path('signUp/',signup),
    
    path('login-<str:name>/',vba_RulesLogin),
    path('<str:name>-recording-voice/',AutheticateUser),


    path('recording-voice-of-<str:name>-<int:num>/',vba_RulesSignup),
    path('read-sentence-<str:name>-<int:num>/',recordingVoiceUser),

    path('noter', include('noter.urls'), name= "noter")
]
