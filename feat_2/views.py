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


def kelola_playlist(request):
    return render(request, 'kelola_playlist.html')

def tambah_playlist(request):
    return render(request, 'tambah_playlist.html')

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
            UP.deskripsi
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
        'songs_in_playlist': songs_in_playlist
    }

    cursor.close()
    conn.close()

    return render(request, "detail_playlist.html", context)


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
