from django.urls import path
from kelola_album_label.views import delete_song, show_list_album, show_list_lagu

app_name = 'kelola-album-label'

urlpatterns = [
    path('list-album/', show_list_album, name='show_album'),
    path('list-lagu/<str:albumID>/', show_list_lagu, name='show_lagu'),
    path('delete-song/<str:kontenID>/<str:albumID>/', delete_song, name='delete_song'),
]