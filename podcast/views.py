from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import psycopg2
from main.connect import get_db_connection
import uuid
import random
from datetime import date
from datetime import datetime

# Create your views here.
def show_detail_podcast(request, user_role, id_podcast):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT judul, tanggal_rilis, tahun FROM KONTEN WHERE id=%s", (id_podcast,))
    konten= cursor.fetchone()
    judul_podcast = konten[0]
    tanggal_podcast = konten[1]
    tahun_podcast = konten[2]

    cursor.execute("SELECT email_podcaster FROM PODCAST WHERE id_konten=%s", (id_podcast,))
    email_podcaster = cursor.fetchone()[0]

    cursor.execute("SELECT genre FROM GENRE WHERE id_konten=%s", (id_podcast,))
    genre_podcast_raw = cursor.fetchall()
    genre_podcast = ''
    for genre in genre_podcast_raw:
        genre_podcast = genre_podcast + genre[0] + ','

    cursor.execute("SELECT nama FROM AKUN WHERE email=%s", (email_podcaster,))
    nama_podcaster = cursor.fetchone()[0]

    cursor.execute("SELECT judul, deskripsi, durasi, tanggal_rilis FROM EPISODE WHERE id_konten_podcast=%s", (id_podcast,))
    daftar_episode = cursor.fetchall()

    durasi_total = 0
    for episode in (daftar_episode):
        durasi_total = durasi_total + episode[2]
    jam_total = durasi_total//60
    menit_total = durasi_total - (jam_total*60)

    print(daftar_episode)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    context = {
        'judul_podcast': judul_podcast,
        'genre_podcast': genre_podcast,
        'nama_podcaster': nama_podcaster,
        'jam_total': jam_total,
        'menit_total':menit_total,
        'tanggal_podcast':tanggal_podcast,
        'tahun_podcast': tahun_podcast,
        'episodes': daftar_episode
    }

    return render(request, "detail.html", context)

def show_chart(request):
    context = {
    }

    return render(request, "chart.html", context)

def show_chart_detail(request):
    context = {
    }

    return render(request, "chart_detail.html", context)

def create_podcast(request):

    conn = get_db_connection()
    cursor = conn.cursor()

    context = {
    }

    return render(request, "create_podcast.html", context)

def show_podcast_list(request):

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        judul_podcast = request.POST.get("title")
        genres = request.POST.get("artist")
        genres_split = genres.split(', ')
        genres_fix = genres_split[1:]
        cursor.execute("SELECT id FROM KONTEN")
        daftar_uuid = cursor.fetchall()
        cek_uuid = True
        currentdate = date.today()
        currentyear = datetime.now().year
        while cek_uuid:
            status = True
            uuid_konten = uuid.uuid4
            for uuid1 in daftar_uuid:
                if uuid1 == uuid_konten:
                    status = False
            if status == True:
                cek_uuid = False
        cursor.execute("INSERT INTO KONTEN VALUES(%s, %s, %s, %s, 0)", (uuid_konten, judul_podcast, currentdate, currentyear,))
        # cursor.execute("INSERT INTO KONTEN VALUES("+uuid_konten+", "+judul_podcast+", "+currentdate+", "+currentyear+", "+ '0'+")") #INSERT KE KONTEN
        for genre in genres_fix: #INSERT GENRE
            cursor.execute("INSERT INTO GENRE VALUES(%s, %s)", (uuid_konten, genre,))
            # cursor.execute("INSERT INTO GENRE VALUES("+uuid_konten+", "+genre+")")
        cursor.execute("INSERT INTO PODCAST VALUES(%s, oduboj_ize83@outlook.com)", (uuid_konten,))
        # cursor.execute("INSERT INTO PODCAST VALUES("+uuid_konten+", oduboj_ize83@outlook.com)")        
    jumlah_episodes = [] 
    cursor.execute("SELECT K.id, K.judul, K.durasi FROM KONTEN K WHERE K.id IN(SELECT id_konten FROM PODCAST WHERE email_podcaster = 'oduboj_ize83@outlook.com')") #TODO: DIRUBAH
    podcasts = cursor.fetchall()
    for podcast in podcasts:
        cursor.execute("SELECT COUNT(id_episode) FROM EPISODE WHERE id_konten_podcast=%s", (podcast[0],))
        jumlah_episodes.append(cursor.fetchone())
    

    cursor.close()
    conn.close()

    merged_podcast = [tup1 + tup2 for tup1, tup2 in zip(podcasts, jumlah_episodes)]

    context = {
        'podcasts': merged_podcast,
    }

    return render(request, "podcast_list.html", context)

def show_create_episode(request):
    context = {
    }

    return render(request, "create_episode.html", context)

def show_episode_list(request):
    context = {
    }

    return render(request, "episode_list.html", context)