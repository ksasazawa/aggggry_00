from django.urls import path
from . import views

app_name = 'aggggry_app'

urlpatterns = [
    path('', views.home, name="home"),
]
