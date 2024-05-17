from django.urls import path
from kelola_album_artist.views import form_album, show_create_album, show_create_lagu, show_create_lagu_songwriter, show_list_album, show_list_lagu

app_name = 'kelola-album-artist'

urlpatterns = [
    path('create-album/', show_create_album, name='show_album'),
    path('create-lagu/', show_create_lagu, name='show_lagu'),
    path('create-lagu-songwriter/', show_create_lagu_songwriter, name='show_lagu_songwriter'),
    path('list-album/', show_list_album, name='show_artist'),
    path('list-lagu/', show_list_lagu, name='show_lagu'),
    path('form-create-album/', form_album, name='form_album'),
]