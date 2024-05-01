from django.urls import path
from cek_royalti.views import show_main

app_name = 'cek-royalti'

urlpatterns = [
    path('', show_main, name='show_main'),
]