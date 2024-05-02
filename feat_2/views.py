from django.shortcuts import render

def kelola_playlist(request):
    return render(request, 'kelola_playlist.html')

def kelola_playlist_terisi(request):
    return render(request, 'kelola_playlist_terisi.html')

def tambah_playlist(request):
    return render(request, 'tambah_playlist.html')

def detail_playlist(request):
    return render(request, 'detail_playlist.html')

def tambah_lagu(request):
    return render(request, 'tambah_lagu.html')

def add_to_playlist(request):
    return render(request, 'add_to_playlist.html')

def download_song(request):
    return render(request, 'download_song.html')

def failed_download(request):
    return render(request, 'failed_download.html')

def failed_message(request):
    return render(request, 'failed_message.html')

def song_detail(request):
    return render(request, 'song_detail.html')

def success_message(request):
    return render(request, 'success_message.html')
