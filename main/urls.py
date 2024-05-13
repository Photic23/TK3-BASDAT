from django.urls import path
from main.views import show_register_pengguna, show_dashboard_podcast, show_register_main,show_register_label
from main.views import login, index
from main.views import show_dashboard_pengguna, show_dashboard

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('register-user/', show_register_pengguna, name='show_register_pegguna'),
    path('dashboard', show_dashboard, name='show_dashboard'),
    path('dashboard-podcast/', show_dashboard_podcast, name='show_dashboard_podcast'),
    path('dashboard-pengguna/', show_dashboard_pengguna, name='show_dashboard_pengguna'),
    path('register/', show_register_main, name='show_register_main'),
    path('register-label/', show_register_label, name='show_register_label'),
]