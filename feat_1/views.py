from django.shortcuts import render

# Create your views here.
def daftar_playlist_page(request):
    context = {}
    
    return render(request, 'daftar-playlist.html', context)

