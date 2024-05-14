from django.urls import path
from kelola_album_artist.views import show_create_album, show_create_lagu, show_create_lagu_songwriter, show_list_album, show_list_lagu

app_name = 'kelola-album-artist'

urlpatterns = [
    path('create-album/<str:user_email>/<str:user_roles>', show_create_album, name='show_album'),
    path('create-lagu/', show_create_lagu, name='show_lagu'),
    path('create-lagu-songwriter/', show_create_lagu_songwriter, name='show_lagu_songwriter'),
    path('list-album/<str:user_email>/<str:user_roles>', show_list_album, name='show_artist'),
    path('list-lagu/', show_list_lagu, name='show_lagu'),
]