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
            cursor.execute("SELECT email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal FROM akun WHERE email = %s AND password = %s", (email, password))
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
            }
            if account is not None:
                request.session['nama'] = user['nama']
                print(user['nama'])
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

def show_dashboard_pengguna(request):
    context = {
    }

    return render(request, "dashboard_pengguna_biasa.html", context)

def show_dashboard(request, akun):
    context = {
        'user': akun,
    }

    return render(request, "dashboard.html", context)

def show_dashboard_podcast(request):
    context = {
    }

    return render(request, "dashboard_podcast.html", context)

def show_register_label(request):
    context = {
    }

    return render(request, "regist_label.html", context)

    