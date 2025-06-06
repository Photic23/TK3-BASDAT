from django.urls import path
from feat_1.views import daftar_playlist_page, add_playlist, search, playlist_detail
from feat_1.views import add_subscription, pay_subscription, subscription_history
from feat_1.views import downloaded_song, delete_from_downloaded

app_name = 'feat_1'

urlpatterns = [
    path('list-playlist', daftar_playlist_page, name='daftar_playlist_page'),
    path('add-playlist/', add_playlist, name='add_playlist'),
    path('add-subscription/', add_subscription, name='add_subscription'),
    path('pay-subscription/', pay_subscription, name='pay_subscription'),
    path('subscription-history/', subscription_history, name='subscription_history'),
    path('search', search, name='search'),
    path('downloaded-song/', downloaded_song, name='downloaded_song'),
    path('playlist-detail/', playlist_detail, name='playlist_detail'),
    path('playlist-detail/', playlist_detail, name='playlist_detail'),
    path('delete-song/<str:id>/', delete_from_downloaded, name='delete_song'),
]