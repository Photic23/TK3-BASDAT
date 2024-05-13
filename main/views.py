from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import psycopg2
from main.connect import get_db_connection

# Create your views here.

def index(request):
    context = {
    }

    return render(request, "landing-page.html", context)

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
            user = {
                'email': account[0],
                'password': account[1],
                'nama': account[2],
                'gender': account[3],
                'tempat_lahir': account[4],
                'tanggal_lahir': account[5],
                'is_verified': account[6],
                'kota_asal': account[7],
                'roles': account[8]
            }
            if account is not None:
                request.session['nama'] = user['nama']
                context = {
                    'user': user,
                }
                return render(request, 'dashboard.html', context)
            else:
                messages.error(request, 'Email or password is incorrect')
                return redirect('main:login')

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

def show_dashboard_pengguna(request, context):


    return render(request, "dashboard_pengguna_biasa.html", context)

def show_dashboard(request, context):

    return render(request, "dashboard.html", context)

def show_dashboard_podcast(request):
    context = {
    }

    return render(request, "dashboard_podcast.html", context)

def show_register_label(request):
    context = {
    }

    return render(request, "regist_label.html", context)

    