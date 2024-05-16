from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import psycopg2
from main.connect import get_db_connection
from utils import context_user
from django.views.decorators.csrf import csrf_exempt
import json
import uuid

def tambah_playlist(request):
    return render(request, 'tambah_playlist.html')

def hapus_playlist(request):
    playlist_id = request.GET.get('playlist_id', None)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Lakukan operasi penghapusan data
    cursor.execute("DELETE FROM USER_PLAYLIST WHERE id_playlist = %s", (playlist_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return HttpResponse(b"DELETED", status=201)

def add_lagu_playlist(request):
    playlist_id = request.GET.get('playlist_id', None)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            k.judul, 
            a.nama 
        FROM 
            SONG s 
        JOIN 
            KONTEN k ON s.id_konten = k.id 
        JOIN 
            ARTIST ar ON s.id_artist = ar.id 
        JOIN 
            AKUN a ON ar.email_akun = a.email
    """)
    songs = cursor.fetchall()
    cursor.close()
    conn.close()

    # Buat daftar lagu-artis dalam format "judul - artis"
    song_artist_list = ["{} - {}".format(song[0], song[1]) for song in songs]

    context = {
        'songs': song_artist_list,
        'playlist_id': playlist_id
    }

    return render(request, "add_lagu_playlist.html", context)

@csrf_exempt
def tambah_lagu(request):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        playlist_name = request.POST.get('playlistName')  # Sesuaikan dengan nama input dalam HTML
        deskripsi = request.POST.get('deskripsi')
        playlist_id =  request.POST.get('playlist_id')
        judul_lagu = request.POST.get('judul_lagu')
        judul_lagu = judul_lagu.split(" - ")[0]

        cursor.execute("SELECT id FROM KONTEN WHERE judul = %s", [judul_lagu])
        id_konten = cursor.fetchone()[0]

        cursor.execute("INSERT INTO PLAYLIST_SONG (id_playlist, id_song) VALUES (%s, %s)", [playlist_id, id_konten])
        
        conn.commit()
        cursor.close()
        conn.close()

        return HttpResponse(b"ADD LAGU", status=201)
    
    return HttpResponseNotFound()

def ubah_playlist(request):
    playlist_id = request.GET.get('playlist_id', None)

    context = {
        'playlist_id': playlist_id
    }

    return render(request, 'ubah_playlist.html', context)

@csrf_exempt
def update_playlist(request):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        playlist_name = request.POST.get('playlistName')  # Sesuaikan dengan nama input dalam HTML
        deskripsi = request.POST.get('deskripsi')
        playlist_id =  request.POST.get('playlist_id')

        cursor.execute("""
            UPDATE USER_PLAYLIST
            SET judul = %s, deskripsi = %s
            WHERE id_playlist = %s
        """, (playlist_name, deskripsi, playlist_id))
        conn.commit()
        
        cursor.close()
        conn.close()

        return HttpResponse(b"UPDATE", status=201)
    
    return HttpResponseNotFound()

    

@csrf_exempt
def form_tambah_playlist(request):
    user = context_user.context_user_getter(request)
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        email_user = user['email']
        playlist_name = request.POST.get('playlistName')  # Sesuaikan dengan nama input dalam HTML
        deskripsi = request.POST.get('deskripsi')
        random_uuid_user_playlist = str(uuid.uuid4())
        random_uuid_playlist = str(uuid.uuid4())
        today_date = datetime.today().date()

        cursor.execute("""
            INSERT INTO PLAYLIST (id)
            VALUES (%s)
        """, (random_uuid_playlist,))

        cursor.execute("""
            INSERT INTO USER_PLAYLIST (email_pembuat, id_user_playlist, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi)
            VALUES (%s, %s, %s, %s, 0, %s, %s, 0)
        """, (email_user, random_uuid_user_playlist, playlist_name, deskripsi, today_date, random_uuid_playlist))

        cursor.execute("SELECT * FROM USER_PLAYLIST")
        playlists = cursor.fetchall()

        for playlist in playlists:
            print(playlist)

        conn.commit()
        
        cursor.close()
        conn.close()

        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()

def detail_playlist(request):
    playlist_id = request.GET.get('playlist_id', None)
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query untuk detail playlist
    query_playlist = """
        SELECT 
            UP.judul,
            A.nama AS pembuat,
            UP.jumlah_lagu,
            UP.total_durasi,
            UP.tanggal_dibuat,
            UP.deskripsi,
            UP.id_playlist
        FROM 
            USER_PLAYLIST UP
        JOIN 
            AKUN A ON UP.email_pembuat = A.email
        WHERE UP.id_playlist = %s
        """
    cursor.execute(query_playlist, (playlist_id,))
    detail_playlist = cursor.fetchall()

    # Query untuk lagu dalam playlist
    query_songs = """
        SELECT 
            K.judul,
            AK.nama,
            K.durasi
        FROM 
            PLAYLIST_SONG PS
        JOIN 
            KONTEN K ON PS.id_song = K.id
        JOIN 
            SONG S ON PS.id_song = S.id_konten
        JOIN 
            ARTIST AR ON S.id_artist = AR.id
        JOIN 
            AKUN AK ON AR.email_akun = AK.email
        WHERE 
            PS.id_playlist = %s
        """
    cursor.execute(query_songs, (playlist_id,))
    songs_in_playlist = cursor.fetchall()

    context = {
        'detail_playlist': detail_playlist,
        'songs_in_playlist': songs_in_playlist,
    }

    cursor.close()
    conn.close()

    return render(request, "detail_playlist.html", context)

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

def kelola_playlist_terisi(request):
    user = context_user.context_user_getter(request)
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT DISTINCT 
            email_pembuat, 
            id_user_playlist, 
            judul, 
            deskripsi, 
            jumlah_lagu, 
            tanggal_dibuat, 
            id_playlist, 
            total_durasi 
        FROM USER_PLAYLIST 
        WHERE email_pembuat = %s;
        """
        
    cursor.execute(query, (user['email'],))
    playlist = cursor.fetchall()

    context = {
        'playlist_query': playlist,
        'user':user
    }

    cursor.close()
    conn.close()
    return render(request, "kelola_playlist_terisi.html", context)
