from django.urls import path
from . import views

app_name = 'buyback_hangar'

urlpatterns = [
    path('', views.corp_hangar, name='view'),
]
