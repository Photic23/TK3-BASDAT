from django.urls import path
from feat_1.views import daftar_playlist_page, add_playlist, add_subscription, pay_subscription

app_name = 'feat_1'

urlpatterns = [
    path('', daftar_playlist_page, name='daftar_playlist_page'),
    path('add-playlist/', add_playlist, name='add_playlist'),
    path('add-subscription/', add_subscription, name='add_subscription'),
    path('pay-subscription/', pay_subscription, name='pay_subscription'),
]