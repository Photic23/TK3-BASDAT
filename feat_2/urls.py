from django.urls import path
from feat_2 import views

app_name = 'feat_2'

urlpatterns = [
    path('tambah_playlist/', views.tambah_playlist, name='tambah_playlist'),
    path('detail_playlist/', views.detail_playlist, name='detail_playlist'),
    path('tambah_lagu/', views.tambah_lagu, name='tambah_lagu'),
    path('kelola_playlist_terisi/', views.kelola_playlist_terisi, name='kelola_playlist_terisi'),
    path('add_to_playlist/', views.add_to_playlist, name='add_to_playlist'),
    path('download_song/', views.download_song, name='download_song'),
    path('failed_download/', views.failed_download, name='failed_download'),
    path('failed_message/', views.failed_message, name='failed_message'),
    path('song_detail/', views.song_detail, name='song_detail'),
    path('success_message/', views.success_message, name='success_message'),
    path('form_tambah_playlist/', views.form_tambah_playlist, name='form_tambah_playlist'),
    path('hapus_playlist/', views.hapus_playlist, name='hapus_playlist'),
    path('ubah_playlist/', views.ubah_playlist, name='ubah_playlist'),
    path('add_lagu_playlist/', views.add_lagu_playlist, name='add_lagu_playlist'),
]
