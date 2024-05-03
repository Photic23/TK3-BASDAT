from django.urls import path
from main.views import show_register_pegguna, show_dashboard_podcast, show_register_main,show_register_label

app_name = 'main'

urlpatterns = [
    path('register-user/', show_register_pegguna, name='show_register_pegguna'),
    path('dashboard-podcast/', show_dashboard_podcast, name='show_dashboard_podcast'),
    path('register/', show_register_main, name='show_register_main'),
    path('register-label/', show_register_label, name='show_register_label'),
]