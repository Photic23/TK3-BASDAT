from django.urls import path
from podcast.views import show_detail_podcast, show_chart, show_chart_detail, create_podcast, show_podcast_list,show_create_episode, show_episode_list, hapus_episode, hapus_podcast

app_name = 'podcast'

urlpatterns = [
    path('detail/<str:id_podcast>/', show_detail_podcast, name='show_detail_podcast'),
    path('chart/', show_chart, name='show_chart'),
    path('chart-detail/<str:id_playlist>/', show_chart_detail, name='show_chart_detail'),
    path('create/', create_podcast, name='create_podcast'),
    path('list/', show_podcast_list, name='show_podcast_list'),
    path('create-episode/<str:id_podcast>/', show_create_episode, name='show_create_episode'),
    path('episode-list/<str:id_podcast>/', show_episode_list, name='show_episode_list'),
    path('hapus-episode/<str:id_podcast>/<str:id_episode>/', hapus_episode, name='hapus_episode'),
    path('hapus-podcast/<str:id_podcast>/', hapus_podcast, name='hapus_podcast'),
]