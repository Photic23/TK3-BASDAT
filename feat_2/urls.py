from django.urls import path
from feat_2 import views

app_name = 'feat_2'

urlpatterns = [
    path('tambah_playlist/', views.tambah_playlist, name='tambah_playlist'),
    path('detail_playlist/', views.detail_playlist, name='detail_playlist'),
    path('tambah_lagu/', views.tambah_lagu, name='tambah_lagu'),
    path('kelola_playlist_terisi/', views.kelola_playlist_terisi, name='kelola_playlist_terisi'),
    # path('song_detail/', views.song_detail, name='song_detail'),
    path('form_tambah_playlist/', views.form_tambah_playlist, name='form_tambah_playlist'),
    path('hapus_playlist/', views.hapus_playlist, name='hapus_playlist'),
    path('ubah_playlist/', views.ubah_playlist, name='ubah_playlist'),
    path('add_lagu_playlist/', views.add_lagu_playlist, name='add_lagu_playlist'),
    path('hapus_lagu/', views.hapus_lagu, name='hapus_lagu'),
]
