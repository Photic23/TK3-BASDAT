import random
import uuid
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from utils import context_user
import psycopg2
from main.connect import get_db_connection
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request, "landing-page.html")

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            connection = get_db_connection()

            cursor = connection.cursor()
            cursor.execute(f"""SELECT
                u.email,
                u.password,
                u.nama,
                u.gender,
                u.tempat_lahir,
                u.tanggal_lahir,
                u.is_verified,
                u.kota_asal,
                COALESCE(
                    STRING_AGG(DISTINCT role, ', '),
                    'Pengguna_biasa'
                ) AS roles,
                CASE
                    WHEN premium.email IS NOT NULL THEN 'Premium'
                    ELSE 'Non_premium'
                END AS premium_status
            FROM
                marmut.AKUN as u
            LEFT JOIN
                (
                    SELECT email_akun AS email_akun, 'Artist' AS role
                    FROM marmut.ARTIST
                    UNION ALL
                    SELECT email AS email_akun, 'Podcaster' AS role
                    FROM marmut.PODCASTER
                    UNION ALL
                    SELECT email_akun AS email_akun, 'Songwriter' AS role
                    FROM marmut.SONGWRITER
                ) AS roles_table ON u.email = roles_table.email_akun
            LEFT JOIN
                (
                    SELECT email
                    FROM marmut.PREMIUM
                ) AS premium ON u.email = premium.email
            WHERE 
                u.email = '{email}' AND u.password = '{password}'
                
            GROUP BY
                u.email,
                u.password,
                u.nama,
                u.gender,
                u.tempat_lahir,
                u.tanggal_lahir,
                u.is_verified,
                u.kota_asal,
                premium.email;""")
            
            account = cursor.fetchone()
            
            if account is not None:
                user = {
                    'email': account[0],
                    'nama': account[2],
                    'roles': account[8],
                    'premium_status': account[9]
                }
                
                request.session['nama'] = user['nama']
                request.session['email'] = user['email']
                request.session['roles'] = user['roles']
                request.session['premium_status'] = user['premium_status']

                return redirect('main:show_dashboard')
            else:
                cursor.execute(f"SELECT * FROM LABEL WHERE email = '{email}' AND password = '{password}';")
                label = cursor.fetchone()
                
                if label is not None:
                    user = {
                        'email': label[2],
                        'nama': label[1],
                        'kontak': label[4],
                        'id': label[0],
                        'id_pemilik_hak_cipta': label[5]
                    }
                    
                    request.session['nama'] = user['nama']
                    request.session['email'] = user['email']
                    request.session['roles'] = None
                    request.session['premium_status'] = None
        
                    return redirect('main:show_dashboard')

                else:    
                    messages.error(request, 'Email or password is incorrect')
                    redirect('main:login')

        except psycopg2.Error as e:
            print(e)
            return HttpResponse("Error occurred while connecting to the database")

        finally:
            if connection:
                cursor.close()
                connection.close()

    else:
        return render(request, 'login-form.html')

def show_register_main(request):
    return render(request, "regist_main.html")

def show_register_pengguna(request):
    return render(request, "regist_pengguna.html")

def show_dashboard(request):
    connection = get_db_connection()
    user = context_user.context_user_getter(request)
    cursor = connection.cursor()
    if user['roles'] is not None: 
        cursor.execute(f"SELECT gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal FROM AKUN WHERE email = '{user['email']}'")
        user_data = cursor.fetchone()
        cursor.execute(f"SELECT k.judul, k.durasi, k.id FROM KONTEN k JOIN SONG ON k.id = SONG.id_konten JOIN ARTIST ON SONG.id_artist = ARTIST.id JOIN AKUN ON ARTIST.email_akun = AKUN.email WHERE ARTIST.email_akun = '{user['email']}';")
        song_data = cursor.fetchall()
        cursor.execute(f"SELECT k.judul, k.durasi, k.id FROM KONTEN k JOIN SONG ON k.id = SONG.id_konten JOIN SONGWRITER_WRITE_SONG ON SONG.id_konten = SONGWRITER_WRITE_SONG.id_song JOIN SONGWRITER ON SONGWRITER.id = SONGWRITER_WRITE_SONG.id_songwriter JOIN AKUN ON SONGWRITER.email_akun = AKUN.email WHERE SONGWRITER.email_akun = '{user['email']}';")
        song_data += cursor.fetchall()
        # cursor.execute(f"SELECT * FROM ALBUM WHERE id_label = '{user_data[0]}';")
        # podcast_data = cursor.fetchall()
        data = {
            'gender': user_data[0],
            'tempat_lahir': user_data[1],
            'tanggal_lahir': user_data[2],
            'is_verified': user_data[3],
            'kota_asal': user_data[4]
        }
        context = {
            'user': user,
            'data': data,
            'song_list': [{
                'id': row[2],
                'judul': row[0],
                'durasi': row[1],
                } for row in song_data],
            # 'album_list': [{
            #     'id': row[0],
            #     'judul': row[1],
            #     'jumlah_lagu': row[2],
            #     'id_label': row[3],
            #     'total_durasi': row[4],
            #     } for row in album_data],
        }
    else:
        cursor.execute(f"SELECT id, kontak, id_pemilik_hak_cipta FROM LABEL WHERE email = '{user['email']}'")
        user_data = cursor.fetchone()
        cursor.execute(f"SELECT * FROM ALBUM WHERE id_label = '{user_data[0]}';")
        album_data = cursor.fetchall()
        data = {
            'id': user_data[0],
            'kontak': user_data[1],
            'pemilik_hak_cipta': user_data[2],
        }
        context = {
            'user': user,
            'data': data,
            'album_list': [{
                'id': row[0],
                'judul': row[1],
                'jumlah_lagu': row[2],
                'id_label': row[3],
                'total_durasi': row[4],
                } for row in album_data],
        }
    
    return render(request, "dashboard.html", context)

def logout(request):
    response = HttpResponseRedirect(reverse('main:login'))
    return response

def show_register_label(request):
    context = {
    }

    return render(request, "regist_label.html", context)

@csrf_exempt
def submit_register_pengguna(request):
    conn = get_db_connection()
    cursor = conn.cursor()

    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kota_asal = request.POST.get('kota_asal')
        roles = request.POST.getlist('role')

        is_verified = bool(roles)

        gender_value = 0
        if gender.lower() == "male":
            gender_value = 1

        try:
            query = """
            INSERT INTO AKUN (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (email, password, name, gender_value, tempat_lahir, tanggal_lahir, is_verified, kota_asal))

            uuid_pemilik_hak_cipta = str(uuid.uuid4())
            random_rate = random.randint(100, 5000)

            target_roles = ["artist", "podcaster", "songwriter"]

            if any(role in target_roles for role in roles):
                cursor.execute("INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti) VALUES (%s, %s)", [uuid_pemilik_hak_cipta, random_rate])
            
            if 'artist' in roles:
                uuid_artist = str(uuid.uuid4())
                cursor.execute("INSERT INTO ARTIST (id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)", [uuid_artist, email, uuid_pemilik_hak_cipta])
            elif 'podcaster' in roles:
                cursor.execute("INSERT INTO PODCASTER (email) VALUES (%s)", [email])
            elif 'songwriter' in roles:
                uuid_songwriter = str(uuid.uuid4())
                cursor.execute("INSERT INTO SONGWRITER (id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)", [uuid_songwriter, email, uuid_pemilik_hak_cipta])
            
            conn.commit()

        except Exception:
            conn.rollback()
            error_message = "Email already exists. Please use a different email."
            if error_message:
                context = {'error_message': error_message}
                return render(request, 'regist_pengguna.html', context)

        cursor.close()
        conn.close()

        return redirect(reverse('main:index'))

@csrf_exempt
def submit_register_label(request):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        uuid_label = str(uuid.uuid4())
        uuid_pemilik_hak_cipta = str(uuid.uuid4())
        random_rate = random.randint(100, 5000)

        cursor.execute("INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti) VALUES (%s, %s)", [uuid_pemilik_hak_cipta, random_rate])

        try:
            query = """
            INSERT INTO LABEL (id, nama, email, password, kontak, id_pemilik_hak_cipta) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (uuid_label, name, email, password, contact, uuid_pemilik_hak_cipta))
            conn.commit()

        except Exception:
            conn.rollback()
            error_message = "Email already exists. Please use a different email."
            if error_message:
                context = {'error_message': error_message}
                return render(request, 'regist_label.html', context)


        cursor.close()
        conn.close()

        context = {
        }

        return redirect(reverse('main:index'))



    