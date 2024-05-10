from django.shortcuts import render

# Create your views here.


def daftar_playlist_page(request):
    context = {
        'username': "Scarletra",
    }
    
    return render(request, 'daftar-playlist.html', context)

def add_playlist(request):
    context = {
        'username': "Scarletra",
    }
    return render(request, 'form-playlist.html', context)

def add_subscription(request):
    context = {
        'username': "Scarletra",
    }
    return render(request, 'langganan-paket.html', context)

def pay_subscription(request):
    context = {
        'username': "Scarletra",
    }
    return render(request, 'pembayaran-paket.html', context)

def subscription_history(request):
    context = {
        'username': "Scarletra",
    }
    return render(request, 'riwayat-langganan.html', context)

def test_searchbar(request):
    context = {
        'username': "Scarletra",
    }
    return render(request, 'search-bar-code.html', context)

def downloaded_song(request):
    context = {
        'username': "Scarletra",
    }
    return render(request, 'downloaded-song.html', context)

def playlist_detail(request):
    context = {
        'username': "Scarletra",
    }
    return render(request, 'playlist-detail.html', context)
