from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register-user/', show_register_pengguna, name='show_register_pegguna'),
    path('dashboard', show_dashboard, name='show_dashboard'),
    path('register/', show_register_main, name='show_register_main'),
    path('register-label/', show_register_label, name='show_register_label'),
    path('register_user/submit_register_pengguna/', submit_register_pengguna, name='submit_register_pengguna'),
    path('register_user/submit_register_label/', submit_register_label, name='submit_register_label'),
]