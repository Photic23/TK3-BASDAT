from django.urls import path
from feat_2 import views

urlpatterns = [
    path('tambah_playlist', views.tambah_playlist, name='tambah_playlist'),
    path('detail_playlist/', views.detail_playlist, name='detail_playlist'),
    path('tambah_lagu/', views.tambah_lagu, name='tambah_lagu'),
    path('kelola_playlist/', views.kelola_playlist, name='kelola_playlist'),
    path('kelola_playlist_terisi/', views.kelola_playlist_terisi, name='kelola_playlist_terisi'),
    path('add_to_playlist/', views.add_to_playlist, name='add_to_playlist'),
    path('download_song/', views.download_song, name='download_song'),
    path('failed_download/', views.failed_download, name='failed_download'),
    path('failed_message/', views.failed_message, name='failed_message'),
    path('song_detail/', views.song_detail, name='song_detail'),
    path('success_message/', views.success_message, name='success_message'),
]
