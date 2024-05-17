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
from psycopg2.errors import UndefinedColumn
from django.db import DatabaseError
from django.urls import reverse
from psycopg2.errors import UniqueViolation

def tambah_playlist(request):
    user = context_user.context_user_getter(request)
    context = {
        'user' : user
    }
    return render(request, "tambah_playlist.html", context)

def hapus_playlist(request):
    playlist_id = request.GET.get('playlist_id', None)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Lakukan operasi penghapusan data
    cursor.execute("DELETE FROM USER_PLAYLIST WHERE id_playlist = %s", (playlist_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(reverse('feat_2:kelola_playlist_terisi'))

def hapus_lagu(request):
    konten_id = request.GET.get('konten_id', None)
    playlist_id = request.GET.get('playlist_id', None)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Lakukan operasi penghapusan data
    cursor.execute("DELETE FROM PLAYLIST_SONG WHERE id_song = %s", (konten_id,))
    cursor.execute("""
            UPDATE USER_PLAYLIST
            FROM KONTEN
            WHERE KONTEN.id = %s AND USER_PLAYLIST.id_playlist = %s
        """, [konten_id, playlist_id])
    conn.commit()

    cursor.close()
    conn.close()
    previous_url = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_url)

def add_lagu_playlist(request):
    playlist_id = request.GET.get('playlist_id', None)
    user = context_user.context_user_getter(request)

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
        'playlist_id': playlist_id,
        'user': user
    }

    return render(request, "add_lagu_playlist.html", context)

@csrf_exempt
def tambah_lagu(request):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        playlist_id =  request.POST.get('playlist_id')
        judul_lagu = request.POST.get('judul_lagu')
        judul_lagu = judul_lagu.split(" - ")[0]

        cursor.execute("SELECT id FROM KONTEN WHERE judul = %s", [judul_lagu])
        id_konten = cursor.fetchone()[0]

        context = {
            'playlist_id' : playlist_id,
            'judul_lagu' : judul_lagu
        }

        try:
            cursor.execute("INSERT INTO PLAYLIST_SONG (id_playlist, id_song) VALUES (%s, %s)", [playlist_id, id_konten])
        
            conn.commit()
            cursor.close()
            conn.close()
        except UniqueViolation:
            return render(request, 'gagal_add_to_playlist.html', context)

        return redirect(f"{reverse('feat_2:detail_playlist')}?playlist_id={playlist_id}")
    
    return redirect(f"{reverse('feat_2:detail_playlist')}?playlist_id={playlist_id}")

def ubah_playlist(request):
    user = context_user.context_user_getter(request)
    playlist_id = request.GET.get('playlist_id', None)

    context = {
        'playlist_id': playlist_id,
        'user': user
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

        return redirect(reverse('feat_2:kelola_playlist_terisi'))
    
    return redirect(reverse('feat_2:kelola_playlist_terisi'))

    

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

        return redirect(reverse('feat_2:kelola_playlist_terisi'))

def detail_playlist(request):
    user = context_user.context_user_getter(request)
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
            UP.id_playlist,
            UP.id_user_playlist
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
            K.durasi,
            K.id
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
        'user' : user
    }

    cursor.close()
    conn.close()

    return render(request, "detail_playlist.html", context)

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
        'user': user
    }

    cursor.close()
    conn.close()
    return render(request, "kelola_playlist_terisi.html", context)

from django.shortcuts import render, redirect

def song_detail(request):
    konten_id = request.GET.get('konten_id', None)
    conn = get_db_connection()
    cursor = conn.cursor()

    user = context_user.context_user_getter(request)

    query = """
        SELECT 
            K.judul,
            G.genre,
            A.nama,
            AW.nama,
            K.durasi,
            K.tanggal_rilis,
            K.tahun,
            S.total_play,
            S.total_download,
            AL.judul
        FROM 
            KONTEN K
        JOIN 
            SONG S ON K.id = S.id_konten
        JOIN 
            ALBUM AL ON S.id_album = AL.id
        JOIN 
            ARTIST ART ON S.id_artist = ART.id
        JOIN 
            AKUN A ON ART.email_akun = A.email
        JOIN 
            SONGWRITER_WRITE_SONG SWS ON K.id = SWS.id_song
        JOIN 
            SONGWRITER SW ON SWS.id_songwriter = SW.id
        JOIN 
            AKUN AS AW ON SW.email_akun = AW.email
        JOIN 
            GENRE G ON K.id = G.id_konten
        WHERE 
            K.id = %s;
    """

    cursor.execute(query, (konten_id,))
    song_detail = cursor.fetchall()
    context = {
        'detail_song': song_detail,
        'konten_id' : konten_id,
        'is_premium': user['premium_status'] == 'Premium',
        'user': user
    }

    cursor.close()
    conn.close()

    return render(request, 'song_detail.html', context)

def add_to_playlist(request):
    user = context_user.context_user_getter(request)
    konten_id = request.GET.get('konten_id', None)
    conn = get_db_connection()
    cursor = conn.cursor()

    query_check_email = """
        SELECT 
            email_pembuat
        FROM 
            USER_PLAYLIST
        WHERE 
            email_pembuat = %s;
    """
    cursor.execute(query_check_email, (user['email'],))
    email_check = cursor.fetchone()

    if not email_check:
        # Jika email tidak ditemukan, redirect ke halaman add_to_playlist
        cursor.close()
        conn.close()
        return redirect('add_to_playlist')

    query_lagu_artist = """
        SELECT 
            KONTEN.judul,
            AKUN.nama
        FROM 
            KONTEN
        JOIN 
            SONG ON KONTEN.id = SONG.id_konten
        JOIN 
            ARTIST ON SONG.id_artist = ARTIST.id
        JOIN 
            AKUN ON ARTIST.email_akun = AKUN.email
        WHERE 
            KONTEN.id = %s;
    """
    cursor.execute(query_lagu_artist, (konten_id,))
    lagu_artist = cursor.fetchall()

    query_user_playlist = """
        SELECT 
            USER_PLAYLIST.judul,
            USER_PLAYLIST.id_playlist
        FROM 
            USER_PLAYLIST
        WHERE 
            USER_PLAYLIST.email_pembuat = %s;
    """
    cursor.execute(query_user_playlist, (user['email'],))
    user_playlist = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    context = {
        'lagu_artist': lagu_artist,
        'user_playlist': user_playlist,
        'konten_id': konten_id,
        'user': user
    }

    return render(request, 'add_to_playlist.html', context)

@csrf_exempt
def insert_to_playlist(request):
    conn = get_db_connection()
    cursor = conn.cursor()
    user = context_user.context_user_getter(request)

    if request.method == 'POST':
        user_playlist =  request.POST.get('user_playlist')
        konten_id = request.POST.get('konten_id')

        query_judul = """
            SELECT 
                KONTEN.judul
            FROM
                KONTEN
            WHERE
                KONTEN.id = %s;
        """
        cursor.execute(query_judul, (konten_id,))
        judul_lagu = cursor.fetchall()

        query_playlist = """
            SELECT 
                USER_PLAYLIST.judul
            FROM
                USER_PLAYLIST
            WHERE
                USER_PLAYLIST.id_playlist = %s;
        """
        cursor.execute(query_playlist, (user_playlist,))
        judul_playlist = cursor.fetchall()

        context = {
            'judul_lagu' : judul_lagu,
            'judul_playlist' : judul_playlist,
            'playlist_id' : user_playlist,
            'konten_id' : konten_id,
            'user': user
        }

        try:
            query_insert = """
                INSERT INTO PLAYLIST_SONG (id_song, id_playlist)
                VALUES (%s, %s);
            """

            cursor.execute(query_insert, [konten_id, user_playlist])

            conn.commit()
            cursor.close()
            conn.close()

            return render(request, 'berhasil_add.html', context)
        
        except UniqueViolation:
            return render(request, 'gagal_add.html', context)
    return render(request, 'berhasil_add.html')

def download(request):
    conn = get_db_connection()
    cursor = conn.cursor()
    konten_id = request.GET.get('konten_id', None)
    user = context_user.context_user_getter(request)

    query_judul = """
        SELECT 
            KONTEN.judul
        FROM
            KONTEN
        WHERE
            KONTEN.id = %s;
    """
    cursor.execute(query_judul, (konten_id,))
    judul = cursor.fetchall()

    context = {
        'judul' : judul,
        'user' : user,
        'konten_id' : konten_id
    }


    try:
        query_insert = """
            INSERT INTO DOWNLOADED_SONG (id_song, email_downloader)
            VALUES (%s, %s);
        """
        cursor.execute(query_insert, (konten_id, user['email'],))

        conn.commit()
        cursor.close()
        conn.close()

        return render(request, 'download.html', context)
    except UniqueViolation:
        return render(request, 'gagal_download.html', context)

def shuffle(request):
    conn = get_db_connection()
    cursor = conn.cursor()
    user_playlist_id = request.GET.get('user_playlist_id', None)
    user = context_user.context_user_getter(request)
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    query_select_email = """
        SELECT
            email_pembuat
        FROM
            USER_PLAYLIST
        WHERE
            id_user_playlist = %s;
    """
    cursor.execute(query_select_email, (user_playlist_id,))
    email_pembuat = cursor.fetchone()[0]

    query_insert_playlist = """
        INSERT INTO AKUN_PLAY_USER_PLAYLIST (email_pemain, id_user_playlist, email_pembuat, waktu)
        VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query_insert_playlist, (user['email'], user_playlist_id, email_pembuat, timestamp))

    query_select_lagu ="""
    SELECT
        PLAYLIST_SONG.id_song
    FROM
        PLAYLIST_SONG
    JOIN
        USER_PLAYLIST ON USER_PLAYLIST.id_playlist = PLAYLIST_SONG.id_playlist
    WHERE
        USER_PLAYLIST.id_user_playlist = %s;
    """
    cursor.execute(query_select_lagu, (user_playlist_id,))
    play_lagu = cursor.fetchall()

    query_insert_song = """
        INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu)
        VALUES (%s, %s, %s)
    """

    for lagu in play_lagu:
        id_song = lagu[0]

        cursor.execute(query_insert_song, (user['email'], id_song, timestamp))


    conn.commit()
    cursor.close()
    conn.close()

    previous_url = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_url)

def play_song(request):
    conn = get_db_connection()
    cursor = conn.cursor()
    konten_id = request.GET.get('konten_id', None)
    user = context_user.context_user_getter(request)
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    query_insert_song = """
        INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query_insert_song, (user['email'], konten_id, timestamp))


    conn.commit()
    cursor.close()
    conn.close()

    previous_url = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_url)

def play(request):
    conn = get_db_connection()
    cursor = conn.cursor()
    konten_id = request.GET.get('konten_id', None)
    user = context_user.context_user_getter(request)
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    query_insert_song = """
        INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query_insert_song, (user['email'], konten_id, timestamp))


    conn.commit()
    cursor.close()
    conn.close()

    previous_url = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_url)

# def play(request):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     konten_id = request.GET.get('konten_id', None)
#     user = context_user.context_user_getter(request)
#     now = datetime.now()
#     timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

#     query_insert_song = """
#         INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu)
#         VALUES (%s, %s, %s)
#     """

#     cursor.execute(query_insert_song, (user['email'], konten_id, timestamp))


#     conn.commit()
#     cursor.close()
#     conn.close()

#     previous_url = request.META.get('HTTP_REFERER', '/')
#     return redirect(previous_url)
