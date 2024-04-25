from django.urls import path
from feat_1.views import daftar_playlist_page

app_name = 'feat_1'

urlpatterns = [
    path('', daftar_playlist_page, name='daftar_playlist_page'),
]