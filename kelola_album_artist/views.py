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

# Create your views here.

def show_create_album(request):
    user = context_user.context_user_getter(request)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT nama, id FROM LABEL")
    label_name = cursor.fetchall()

    cursor.execute("SELECT nama, id, a.email_akun FROM ARTIST A, AKUN AK WHERE ak.email=a.email_akun")
    artists_name = cursor.fetchall()

    cursor.execute("SELECT nama, id, s.email_akun FROM SONGWRITER S, AKUN AK WHERE ak.email=s.email_akun")
    songwriters_name = cursor.fetchall()

    cursor.execute("SELECT DISTINCT genre FROM GENRE")
    genres = cursor.fetchall()

    user_artis_id = ""
    for artist in artists_name:
        email = artist[2]
        if(email == user['email']):
            user_artis_id = artist[1]
            break

    # Close the cursor and connection
    cursor.close()
    conn.close()
    context = {
        'label_name': label_name,
        'artists_name': artists_name,
        'songwriters_name': songwriters_name,
        'genres': genres,
        'user': user,
        'user_id': user_artis_id
    }

    return render(request, "create_album.html", context)

@csrf_exempt
def form_album(request):
    user = context_user.context_user_getter(request)
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(b"Invalid JSON", status=400)
        
        album_name = data.get('albumName')
        label_name = data.get('labelName')
        artist_name = data.get('artistName')
        song_name = data.get('songName')
        songwriters = data.get('songwriters')
        genres = data.get('genres')
        durasi = int(data.get('durasi'))
        random_uuid = str(uuid.uuid4())
        cursor.execute("INSERT INTO ALBUM (id, judul, jumlah_lagu, id_label, total_durasi) VALUES (%s, %s, 1, %s, %s)", (random_uuid, album_name, label_name, durasi))
        conn.commit()

        random_uuid_song = str(uuid.uuid4())
        today_date = datetime.today().date()
        formatted_date = today_date.strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi) VALUES (%s, %s, %s, %s, %s)", (random_uuid_song, song_name, formatted_date, str(today_date.year), durasi))
        conn.commit()

        for genre in genres:
            cursor.execute("INSERT INTO GENRE (id_konten, genre) VALUES (%s, %s)", (random_uuid_song, genre))
            conn.commit()

        cursor.execute("INSERT INTO SONG (id_konten, id_artist, id_album, total_play, total_download) VALUES (%s, %s, %s, 0, 0)", (random_uuid_song, artist_name, random_uuid))
        conn.commit()

        for writer in songwriters:
            cursor.execute("INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song) VALUES (%s, %s)", (writer, random_uuid_song))
            conn.commit()
        
        cursor.close()
        conn.close()

        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()

def delete_album(request, albumID):
    user = context_user.context_user_getter(request)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM ALBUM WHERE id=%s", (albumID,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('kelola-album-artist:show_artist')

def delete_song(request, kontenID):
    user = context_user.context_user_getter(request)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM KONTEN WHERE id=%s", (kontenID,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('kelola-album-artist:show_lagu')

def show_create_lagu(request):
    user = context_user.context_user_getter(request)
    album_id = request.GET.get('album_title', None)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT judul FROM album WHERE id = %s", (album_id,))
    album_name = cursor.fetchone()[0]

    cursor.execute("SELECT nama, id, a.email_akun FROM ARTIST A, AKUN AK WHERE ak.email=a.email_akun")
    artists_name = cursor.fetchall()

    cursor.execute("SELECT nama, id, s.email_akun FROM SONGWRITER S, AKUN AK WHERE ak.email=s.email_akun")
    songwriters_name = cursor.fetchall()

    cursor.execute("SELECT DISTINCT genre FROM GENRE")
    genres = cursor.fetchall()

    user_artis_id = ""
    for artist in artists_name:
        email = artist[2]
        if(email == user['email']):
            user_artis_id = artist[1]
            break

    # Close the cursor and connection
    cursor.close()
    conn.close()
    context = {
        'judul_album': album_name,
        'album_id': album_id,
        'artists_name': artists_name,
        'songwriters_name': songwriters_name,
        'genres': genres,
        'user': user,
        'user_id': user_artis_id
    }

    return render(request, "create_lagu.html", context)

@csrf_exempt
def form_song(request):
    user = context_user.context_user_getter(request)
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(b"Invalid JSON", status=400)
        
        album_id = data.get('albumID')
        artist_name = data.get('artistName')
        song_name = data.get('songName')
        songwriters = data.get('songwriters')
        genres = data.get('genres')
        durasi = int(data.get('durasi'))

        random_uuid_song = str(uuid.uuid4())
        today_date = datetime.today().date()
        formatted_date = today_date.strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi) VALUES (%s, %s, %s, %s, %s)", (random_uuid_song, song_name, formatted_date, str(today_date.year), durasi))
        conn.commit()

        for genre in genres:
            cursor.execute("INSERT INTO GENRE (id_konten, genre) VALUES (%s, %s)", (random_uuid_song, genre))
            conn.commit()

        cursor.execute("INSERT INTO SONG (id_konten, id_artist, id_album, total_play, total_download) VALUES (%s, %s, %s, 0, 0)", (random_uuid_song, artist_name, album_id))
        conn.commit()

        for writer in songwriters:
            cursor.execute("INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song) VALUES (%s, %s)", (writer, random_uuid_song))
            conn.commit()
        
        cursor.close()
        conn.close()

        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()

def show_list_album(request):
    user = context_user.context_user_getter(request)
    conn = get_db_connection()
    cursor = conn.cursor()

    album = ""
    if user['roles'] == "Artist":
        cursor.execute("SELECT id FROM ARTIST A WHERE a.email_akun=%s", (user['email'],))
        id_artist = cursor.fetchone()

        cursor.execute("SELECT DISTINCT judul, jumlah_lagu, total_durasi, l.nama, album.id FROM ALBUM, LABEL L, SONG S WHERE l.id = id_label AND s.id_artist=%s AND album.id=s.id_album", (id_artist,))
        album = cursor.fetchall()
    elif user['roles'] == "Songwriter":
        cursor.execute("SELECT id FROM SONGWRITER S WHERE s.email_akun=%s", (user['email'],))
        id_songwriter = cursor.fetchone()

        cursor.execute("SELECT DISTINCT judul, jumlah_lagu, total_durasi, l.nama, album.id FROM ALBUM, LABEL L, SONGWRITER_WRITE_SONG S, SONG O WHERE l.id = id_label AND s.id_songwriter=%s AND album.id=o.id_album AND s.id_song=o.id_konten", (id_songwriter,))
        album = cursor.fetchall()
    else:
        cursor.execute("SELECT id FROM SONGWRITER S WHERE s.email_akun=%s", (user['email'],))
        id_songwriter = cursor.fetchone()

        cursor.execute("SELECT id FROM ARTIST A WHERE a.email_akun=%s", (user['email'],))
        id_artist = cursor.fetchone()

        cursor.execute("SELECT DISTINCT judul, jumlah_lagu, total_durasi, l.nama, album.id FROM ALBUM, LABEL L, SONGWRITER_WRITE_SONG S, SONG O WHERE l.id = id_label AND s.id_songwriter=%s AND album.id=o.id_album AND s.id_song=o.id_konten AND o.id_artist=%s", (id_songwriter, id_artist,))
        album = cursor.fetchall()

    context = {
        'album_query': album,
        'user':user
    }
    cursor.close()
    conn.close()
    return render(request, "list_album.html", context)

def show_list_lagu(request):
    album_id = request.GET.get('album_title', None)
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
    }

    return render(request, "list_lagu.html", context)