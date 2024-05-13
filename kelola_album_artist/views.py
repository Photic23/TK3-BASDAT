from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import psycopg2
from main.connect import get_db_connection
# Create your views here.

def show_create_album(request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nama FROM LABEL")
    label_name = cursor.fetchall()
    cursor.close()
    conn.close()

    context = {
        'label_name': label_name
    }

    return render(request, "create_album.html", context)

def show_create_lagu(request):
    context = {
    }

    return render(request, "create_lagu_artist.html", context)

def show_create_lagu_songwriter(request):
    context = {
    }

    return render(request, "create_lagu_songwriter.html", context)


def show_list_album(request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT judul, jumlah_lagu, total_durasi, l.nama, album.id FROM ALBUM, LABEL L WHERE l.id = id_label")
    album = cursor.fetchall()
    cursor.close()
    conn.close()
    
    context = {
        'album_query': album
    }

    return render(request, "list_album.html", context)

def show_list_lagu(request):
    album_id = request.GET.get('album_title', None)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT judul FROM album WHERE id = %s", (album_id,))
    album_name = cursor.fetchone()[0]

    cursor.execute("SELECT k.judul, k.durasi, s.total_play, s.total_download FROM SONG s, KONTEN k WHERE s.id_konten=k.id AND s.id_album = %s", (album_id,))
    songs = cursor.fetchall()

    cursor.close()
    conn.close()

    context = {
        'judul_album': album_name,
        'song_query': songs
    }

    return render(request, "list_lagu.html", context)