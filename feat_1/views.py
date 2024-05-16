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

    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM AKUN_PLAY_USER_PLAYLIST WHERE email_pemain = '{email}'")
    playlist_data = cursor.fetchall()
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

@require_http_methods(['GET'])
def subscription_history(request):
    user = context_user.context_user_getter(request)
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT jenis_paket, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal FROM TRANSACTION WHERE email = '{user['email']}'")
    data_langganan = cursor.fetchall()
    context = {
        'data_langganan': [{
            'jenis_paket': row[0],
            'timestamp_dimulai': row[1],
            'timestamp_berakhir': row[2],
            'metode_bayar': row[3],
            'nominal': row[4],
            } for row in data_langganan],
        'user': user,
    }
    return render(request, 'riwayat-langganan.html', context)

def search(request):
    user = context_user.context_user_getter(request)
    query = request.GET.get('query')
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT judul, AKUN.nama, k.id FROM KONTEN k JOIN SONG ON k.id = SONG.id_konten JOIN ARTIST ON SONG.id_artist = ARTIST.id JOIN AKUN ON AKUN.email = ARTIST.email_akun WHERE k.judul ILIKE '%{query}%';")
    list_lagu = cursor.fetchall()
    cursor.execute(f"SELECT judul, AKUN.nama, k.id FROM KONTEN k JOIN PODCAST ON k.id = PODCAST.id_konten JOIN PODCASTER ON PODCAST.email_podcaster = PODCASTER.email JOIN AKUN ON AKUN.email = PODCASTER.email WHERE k.judul ILIKE '%{query}%';")
    list_podcast = cursor.fetchall()
    cursor.execute(f"SELECT judul, AKUN.nama, id_user_playlist FROM USER_PLAYLIST p JOIN AKUN ON AKUN.email = p.email_pembuat WHERE p.judul ILIKE '%{query}%';")
    list_playlist = cursor.fetchall()

    context = {
        'query': query,
        'song_list': [{
                'judul': row[0],
                'artist_name': row[1],
                'id': row[2]
                } for row in list_lagu],
        'podcast_list': [{
                'judul': row[0],
                'podcaster_name': row[1],
                'id': row[2]
                } for row in list_podcast],
        'playlist_list': [{
                'judul': row[0],
                'user_name': row[1],
                'id': row[2]
                } for row in list_playlist],
        'user': user
    }
    return render(request, 'hasil-pencarian.html', context)

def delete_from_downloaded(request, id):
    user = context_user.context_user_getter(request)
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE SONG SET total_download = total_download - 1 WHERE id_konten = '{id}';")
    connection.commit()
    cursor.execute(f"DELETE FROM DOWNLOADED_SONG WHERE id_song = '{id}' AND email_downloader = '{user['email']}';")
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect('feat_1:downloaded_song')

def downloaded_song(request):
    user = context_user.context_user_getter(request)
    if user['premium_status'] == "Premium":
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT KONTEN.judul AS song_title, AKUN.nama AS artist_name, d.id_song as id FROM DOWNLOADED_SONG d JOIN SONG ON d.id_song = SONG.id_konten JOIN KONTEN ON SONG.id_konten = KONTEN.id JOIN ARTIST ON SONG.id_artist = ARTIST.id JOIN AKUN on ARTIST.email_akun = AKUN.email WHERE d.email_downloader = '{user['email']}';")
        downloaded_song = cursor.fetchall()
        context = {
            'song_list': [{
                'song_title': row[0],
                'artist_name': row[1],
                'id': row[2]
                } for row in downloaded_song],
            'user': user,
        }
        cursor.close()
        connection.close()
        return render(request, 'downloaded-song.html', context)
    else:
        return redirect('main:show_dashboard')

def playlist_detail(request):
    context = {
        'username': "Scarletra",
    }
    return render(request, 'playlist-detail.html', context)
