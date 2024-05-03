from django.urls import path
from kelola_album_label.views import show_list_album, show_list_lagu

app_name = 'kelola-album-label'

urlpatterns = [
    path('list-album/', show_list_album, name='show_album'),
    path('list-lagu/', show_list_lagu, name='show_lagu'),
]