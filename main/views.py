from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from utils import context_user
import psycopg2
from main.connect import get_db_connection

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
    context = {
    }

    return render(request, "regist_main.html", context)

def show_register_pengguna(request):
    context = {
    }

    return render(request, "regist.html", context)

def show_dashboard(request):
    connection = get_db_connection()
    user = context_user.context_user_getter(request)
    cursor = connection.cursor()
    if user['roles'] is not None: 
        cursor.execute(f"SELECT gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal FROM AKUN WHERE email = '{user['email']}'")
        user_data = cursor.fetchone()
        data = {
            'gender': user_data[0],
            'tempat_lahir': user_data[1],
            'tanggal_lahir': user_data[2],
            'is_verified': user_data[3],
            'kota_asal': user_data[4]
        }
        context = {
            'user': user,
            'data': data
        }
    else:
        cursor.execute(f"SELECT id, kontak, id_pemilik_hak_cipta FROM LABEL WHERE email = '{user['email']}'")
        user_data = cursor.fetchone()
        data = {
            'id': user_data[0],
            'kontak': user_data[1],
            'pemilik_hak_cipta': user_data[2],
        }
        context = {
            'user': user,
            'data': data
        }
    
    return render(request, "dashboard.html", context)

def show_register_label(request):
    context = {
    }

    return render(request, "regist_label.html", context)

    