from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.connect import get_db_connection
from django.views.decorators.http import require_http_methods
from utils import context_user

# Create your views here.

def daftar_playlist_page(request):
    user = context_user.context_user_getter(request)
    email = user['email']
    connection = get_db_connection()
    print(email)

    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM AKUN_PLAY_USER_PLAYLIST WHERE email_pemain = '{email}'")
    playlist_data = cursor.fetchall()
    print(playlist_data)
    context = {
        'playlist_data': playlist_data,
        'user_name': user['nama']
    }
    
    return render(request, 'daftar-playlist.html', context)

def add_playlist(request):
    context = {
        'username': "Scarletra",
    }
    return render(request, 'form-playlist.html', context)

def add_subscription(request):
    user = context_user.context_user_getter(request)
    context = {
        'user': user
    }
    return render(request, 'langganan-paket.html', context)

@require_http_methods(['GET', 'POST'])
def pay_subscription(request):
    if request.method == 'POST':
        jenis_paket = request.POST['jenis_paket']
        harga = request.POST['harga_paket']
        metode_pembayaran = request.POST['payment']
        
        print(jenis_paket)
        print(harga)
        print(metode_pembayaran)
        
        return redirect('main:show_dashboard')
    
    else:
        package = request.GET.get('package')
        if package:
            
            connection = get_db_connection()
            cursor = connection.cursor()
            print(package)
            cursor.execute(f"SELECT jenis, harga FROM PAKET WHERE jenis = '{package}'")
            paket = cursor.fetchone()
            cursor.close()
            connection.close()
            
            data_paket = {
                'jenis': paket[0],
                'harga': paket[1],
            }

            context = {
                'data_paket': data_paket
            }

            return render(request, "pembayaran-paket.html", context)
        else:
            return HttpResponse("No package selected.")

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
    user = context_user.context_user_getter(request)
    if user['premium_status'] == "Premium":
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM DOWNLOADED_SONG WHERE email_downloader = '{user['email']}'")
        downloaded_song = cursor.fetchall()
        print(downloaded_song)
        cursor.close()
        connection.close()
        return render(request, 'downloaded-song.html', user)
    else:
        return redirect('main:show_dashboard')

def playlist_detail(request):
    context = {
        'username': "Scarletra",
    }
    return render(request, 'playlist-detail.html', context)
