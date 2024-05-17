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
from utils import context_user

# Create your views here.
def show_detail_podcast(request, id_podcast):

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

    conn = get_db_connection()
    cursor = conn.cursor()

    chart_id = []
    cursor.execute("SELECT tipe, id_playlist FROM CHART")
    charts = cursor.fetchall()

    for chart in charts:
        chart_id.append((str(chart[1]),))
    
    merged_chart = [tup1 + tup2 for tup1, tup2 in zip(charts, chart_id)]
    print(merged_chart)
    context = {
        'charts':merged_chart
    }

    cursor.close()
    conn.close()

    return render(request, "chart.html", context)

def show_chart_detail(request, id_playlist):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT B.nama, temp3.judul, temp3.total_play, temp3.tanggal_rilis, temp3.id FROM AKUN B RIGHT JOIN (SELECT A.email_akun, temp2.judul, temp2.tanggal_rilis, temp2.total_play, temp2.id FROM ARTIST A RIGHT JOIN (SELECT K.judul, K.tanggal_rilis, temp.id_artist, temp.total_play, K.id FROM KONTEN K JOIN (SELECT id_konten, id_artist, total_play FROM SONG WHERE id_konten IN(SELECT id_song FROM PLAYLIST_SONG WHERE id_playlist=%s) ORDER BY total_play DESC) temp ON K.id = temp.id_konten) temp2 ON A.id=temp2.id_artist) temp3 ON B.email = temp3.email_akun ORDER BY temp3.total_play DESC;", (id_playlist,))
    details = cursor.fetchall()
    id_song = []
    for detail in details:
        id_song.append((str(detail[4]),))
    merged_detail = [tup1 + tup2 for tup1, tup2 in zip(details, id_song)]    
    print(merged_detail)
    context = {
        'details':merged_detail
    }

    cursor.close()
    conn.close()

    return render(request, "chart_detail.html", context)

def create_podcast(request):

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
            uuid_konten = uuid.uuid4()
            for uuid1 in daftar_uuid:
                if uuid1 == uuid_konten:
                    status = False
            if status == True:
                cek_uuid = False

        cursor.execute("INSERT INTO KONTEN VALUES('{}', '{}', '{}', {}, 0)".format(uuid_konten, judul_podcast, currentdate, currentyear,))
        conn.commit()
        # cursor.execute("INSERT INTO KONTEN VALUES("+uuid_konten+", "+judul_podcast+", "+currentdate+", "+currentyear+", "+ '0'+")") #INSERT KE KONTEN
        for genre in genres_fix: #INSERT GENRE
            cursor.execute("INSERT INTO GENRE VALUES('{}', '{}')".format(str(uuid_konten), genre,))
            conn.commit()
            # cursor.execute("INSERT INTO GENRE VALUES("+uuid_konten+", "+genre+")")
        cursor.execute("INSERT INTO PODCAST VALUES('{}', 'oduboj_ize83@outlook.com')".format(str(uuid_konten),))
        conn.commit()

    context = {
    }

    cursor.close()
    conn.close()

    return render(request, "create_podcast.html", context)

def show_podcast_list(request):

    conn = get_db_connection()
    cursor = conn.cursor()

    user = context_user.context_user_getter(request)
    email = user['email']
    jumlah_episodes = [] 
    podcast_id = []
    cursor.execute("SELECT K.id, K.judul, K.durasi FROM KONTEN K WHERE K.id IN(SELECT id_konten FROM PODCAST WHERE email_podcaster = %s)", (email,)) #TODO: DIRUBAH
    podcasts = cursor.fetchall()
    for podcast in podcasts:
        cursor.execute("SELECT COUNT(id_episode) FROM EPISODE WHERE id_konten_podcast=%s", (podcast[0],))
        jumlah_episodes.append(cursor.fetchone())
        podcast_id.append((str(podcast[0]),))
    

    cursor.close()
    conn.close()

    merged_podcast = [tup1 + tup2 for tup1, tup2 in zip(podcasts, jumlah_episodes)]
    merged_podcast2 = [tup1 + tup2 for tup1, tup2 in zip(merged_podcast, podcast_id)]
    print(merged_podcast2)
    context = {
        'podcasts': merged_podcast2,
    }

    return render(request, "podcast_list.html", context)

def show_create_episode(request, id_podcast):

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        judul_episode = request.POST.get("title")
        deskripsi = request.POST.get("description")
        duration = request.POST.get("duration")
        id_podcast = request.POST.get("id_podcast")
        cursor.execute("SELECT id_episode FROM EPISODE")
        daftar_uuid = cursor.fetchall()
        cek_uuid = True
        currentdate = date.today()
        while cek_uuid:
            status = True
            uuid_konten = uuid.uuid4()
            for uuid1 in daftar_uuid:
                if uuid1 == uuid_konten:
                    status = False
            if status == True:
                cek_uuid = False    
                cursor.execute("INSERT INTO EPISODE VALUES('{}', '{}', '{}', '{}', {}, '{}')".format(uuid_konten, id_podcast, judul_episode, deskripsi, duration, currentdate))
                conn.commit()
        # cursor.execute("INSERT INTO PODCAST VALUES("+uuid_konten+", oduboj_ize83@outlook.com)")        

    cursor.close()
    conn.close()

    context = {
        'id_podcast': id_podcast
    }

    return render(request, "create_episode.html", context)

def show_episode_list(request, id_podcast):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_episode, judul, deskripsi, durasi, tanggal_rilis FROM EPISODE WHERE id_konten_podcast=%s", (id_podcast,))
    episodes = cursor.fetchall()
    episodes_id = []
    for episode in episodes:
        episodes_id.append((str(episode[0]),))

    cursor.close()
    conn.close()

    merged_episodes = [tup1 + tup2 for tup1, tup2 in zip(episodes, episodes_id)]

    context = {
        'episodes': merged_episodes,
        'id_podcast': id_podcast
    }

    return render(request, "episode_list.html", context)

def hapus_episode(request, id_episode, id_podcast):

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute("DELETE FROM EPISODE WHERE id_episode = %s", (id_episode,))
        conn.commit()

    cursor.close()
    conn.close()


    return redirect('../../episode-list/'+id_podcast+'/')


def hapus_podcast(request, id_podcast): #TODO TAMBAHIN EMAIL

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM KONTEN WHERE id=%s", (id_podcast,))
    conn.commit()
    # cursor.execute("SELECT id_episode, judul, deskripsi, durasi, tanggal_rilis FROM EPISODE WHERE id_konten_podcast=%s", (id_podcast,))
    # episodes = cursor.fetchall()
    # episodes_id = []
    # for episode in episodes:
    #     episodes_id.append((str(episode[0]),))

    cursor.close()
    conn.close()

    # merged_episodes = [tup1 + tup2 for tup1, tup2 in zip(episodes, episodes_id)]


    # context = {
    #     'episodes': merged_episodes,
    #     'id_podcast': id_podcast
    # }

    return redirect('../../list/')