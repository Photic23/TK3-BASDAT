from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import psycopg2
from main.connect import get_db_connection
from utils import context_user

# Create your views here.
def show_main(request):
    user = context_user.context_user_getter(request)
    conn = get_db_connection()
    cursor = conn.cursor()
    royalti = ""
    if user['roles'] == "Artist":
        cursor.execute("""SELECT k.judul, a.judul, s.total_play, s.total_download, 
                            s.total_play * phc.rate_royalti AS royalties 
                        FROM KONTEN k
                        JOIN SONG s ON s.id_konten = k.id
                        JOIN ALBUM a ON s.id_album = a.id
                        JOIN ARTIST r ON s.id_artist = r.id
                        JOIN PEMILIK_HAK_CIPTA phc ON r.id = s.id_artist
                        JOIN ROYALTI rt ON rt.id_pemilik_hak_cipta = phc.id AND rt.id_song = s.id_konten
                        WHERE r.email_akun = %s""", (user['email'],))
        royalti = cursor.fetchall()
    elif user['roles'] == "Songwriter":
        cursor.execute("""SELECT k.judul, a.judul, s.total_play, s.total_download, 
                            s.total_play * phc.rate_royalti AS royalties 
                        FROM KONTEN k
                        JOIN SONG s ON s.id_konten = k.id
                        JOIN ALBUM a ON s.id_album = a.id
                        JOIN SONGWRITER_WRITE_SONG r ON s.id_konten = r.id_song
                        JOIN SONGWRITER sr ON sr.id = r.id_songwriter
                        JOIN PEMILIK_HAK_CIPTA phc ON phc.id = sr.id_pemilik_hak_cipta
                        JOIN ROYALTI rt ON rt.id_pemilik_hak_cipta = phc.id AND rt.id_song = s.id_konten
                        WHERE sr.email_akun = %s""", (user['email'],))
        royalti = cursor.fetchall()
    elif user['roles'] == None:
        cursor.execute("""SELECT k.judul, a.judul, s.total_play, s.total_download, 
        s.total_play * phc.rate_royalti AS royalties 
        FROM KONTEN k
        JOIN SONG s ON s.id_konten = k.id
        JOIN ALBUM a ON s.id_album = a.id
        JOIN LABEL l ON a.id_label = l.id
        JOIN PEMILIK_HAK_CIPTA phc ON l.id = a.id_label
        JOIN ROYALTI rt ON rt.id_pemilik_hak_cipta = phc.id AND rt.id_song = s.id_konten
        WHERE l.email = %s""", (user['email'],))
        royalti = cursor.fetchall()
    else:
        cursor.execute("""SELECT k.judul, a.judul, s.total_play, s.total_download, 
                            s.total_play * phc.rate_royalti AS royalties 
                        FROM KONTEN k
                        JOIN SONG s ON s.id_konten = k.id
                        JOIN ALBUM a ON s.id_album = a.id
                        JOIN ARTIST r ON s.id_artist = r.id
                        JOIN SONGWRITER_WRITE_SONG r ON s.id_konten = r.id_song
                        JOIN SONGWRITER sr ON sr.id = r.id_songwriter
                        JOIN PEMILIK_HAK_CIPTA phc ON phc.id = sr.id_pemilik_hak_cipta
                        JOIN ROYALTI rt ON rt.id_pemilik_hak_cipta = phc.id AND rt.id_song = s.id_konten
                        WHERE sr.email_akun = %s""", (user['email'],))
        royalti = cursor.fetchall()

    cursor.close()
    conn.close()

    context = {
        'royalti_query': royalti,
        'user': user
    }

    return render(request, "list_royalti.html", context)