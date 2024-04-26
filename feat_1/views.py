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