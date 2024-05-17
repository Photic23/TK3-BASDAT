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
from django.urls import reverse

# Create your views here.
def show_list_album(request):
    user = context_user.context_user_getter(request)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM LABEL WHERE email=%s", (user['email'],))
    userID = cursor.fetchone()

    cursor.execute("SELECT DISTINCT judul, jumlah_lagu, total_durasi, l.nama, album.id FROM ALBUM, LABEL L, SONG S WHERE l.id = id_label AND l.id=%s AND album.id=s.id_album", (userID,))
    album = cursor.fetchall()

    conn.close()
    cursor.close()
    context = {
        'user': user,
        'album_query': album,
    }

    return render(request, "list_album_label.html", context)

def show_list_lagu(request, albumID):
    album_id = albumID
    user = context_user.context_user_getter(request)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT judul FROM album WHERE id = %s", (album_id,))
    album_name = cursor.fetchone()[0]

    cursor.execute("SELECT k.judul, k.durasi, s.total_play, s.total_download, k.id FROM SONG s, KONTEN k WHERE s.id_konten=k.id AND s.id_album = %s", (album_id,))
    songs = cursor.fetchall()

    cursor.close()
    conn.close()

    context = {
        'judul_album': album_name,
        'song_query': songs,
        'user': user,
        'album_id': album_id,
    }

    return render(request, "list_lagu_label.html", context)

def delete_song(request, kontenID, albumID):
    user = context_user.context_user_getter(request)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM KONTEN WHERE id=%s", (kontenID,))
    conn.commit()
    cursor.close()
    conn.close()


    url = reverse('kelola-album-label:show_lagu', kwargs={'albumID': albumID})

    return redirect(url)