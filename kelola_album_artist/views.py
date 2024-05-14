from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import psycopg2
from main.connect import get_db_connection
# Create your views here.

def show_create_album(request, user_email, user_roles):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute all queries using a single cursor
    cursor.execute("SELECT nama, id FROM LABEL")
    label_name = cursor.fetchall()

    cursor.execute("SELECT nama FROM AKUN WHERE email=%s", (user_email,))
    self_name = cursor.fetchone()

    cursor.execute("SELECT nama, id FROM ARTIST A, AKUN AK WHERE ak.email=a.email_akun")
    artists_name = cursor.fetchall()

    cursor.execute("SELECT nama, id, s.email_akun FROM SONGWRITER S, AKUN AK WHERE ak.email=s.email_akun")
    songwriters_name = cursor.fetchall()

    cursor.execute("SELECT DISTINCT genre FROM GENRE")
    genres = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    context = {
        'label_name': label_name,
        'user_roles': user_roles,
        'self_name': self_name[0],
        'artists_name': artists_name,
        'songwriters_name': songwriters_name,
        'user_email': user_email,
        'genres': genres
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


def show_list_album(request, user_email, user_roles):
    conn = get_db_connection()
    cursor = conn.cursor()
    cur2 = conn.cursor()
    cur3 = conn.cursor()
    album = ""
    if user_roles == "Artist":
        cur2.execute("SELECT id FROM ARTIST A WHERE a.email_akun=%s", (user_email,))
        id_artist = cur2.fetchone()
        cursor.execute("SELECT DISTINCT judul, jumlah_lagu, total_durasi, l.nama, album.id FROM ALBUM, LABEL L, SONG S WHERE l.id = id_label AND s.id_artist=%s AND album.id=s.id_album", (id_artist,))
        album = cursor.fetchall()
    elif user_roles == "Songwriter":
        cur2.execute("SELECT id FROM SONGWRITER S WHERE s.email_akun=%s", (user_email,))
        id_songwriter = cur2.fetchone()
        cursor.execute("SELECT DISTINCT judul, jumlah_lagu, total_durasi, l.nama, album.id FROM ALBUM, LABEL L, SONGWRITER_WRITE_SONG S, SONG O WHERE l.id = id_label AND s.id_songwriter=%s AND album.id=o.id_album AND s.id_song=o.id_konten", (id_songwriter,))
        album = cursor.fetchall()
    else:
        cur2.execute("SELECT id FROM SONGWRITER S WHERE s.email_akun=%s", (user_email,))
        cur3.execute("SELECT id FROM ARTIST A WHERE a.email_akun=%s", (user_email,))
        id_songwriter = cur2.fetchone()
        id_artist = cur3.fetchone()
        cursor.execute("SELECT DISTINCT judul, jumlah_lagu, total_durasi, l.nama, album.id FROM ALBUM, LABEL L, SONGWRITER_WRITE_SONG S, SONG O WHERE l.id = id_label AND s.id_songwriter=%s AND album.id=o.id_album AND s.id_song=o.id_konten AND o.id_artist=%s", (id_songwriter, id_artist,))
        album = cursor.fetchall()
    context = {
        'album_query': album,
        'user_email': user_email,
        'user_roles': user_roles
    }
    cursor.close()
    conn.close()
    cur2.close()
    cur3.close()
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