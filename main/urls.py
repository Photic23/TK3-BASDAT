from django.urls import path
from main.views import show_register

app_name = 'main'

urlpatterns = [
    path('register/', show_register, name='show_register'),

]