from django.urls import path
from kelola_album_artist.views import form_song, delete_song, delete_album, form_album, show_create_album, show_create_lagu, show_list_album, show_list_lagu

app_name = 'kelola-album-artist'

urlpatterns = [
    path('create-album/', show_create_album, name='show_album'),
    path('create-lagu/', show_create_lagu, name='create_lagu'),
    path('list-album/', show_list_album, name='show_artist'),
    path('list-lagu/', show_list_lagu, name='show_lagu'),
    path('form-create-album/', form_album, name='form_album'),
    path('delete-album/<str:albumID>/', delete_album, name='delete_album'),
    path('delete-song/<str:kontenID>/', delete_song, name='delete_song'),
    path('form-create-song/', form_song, name='form_song'),
]