from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import psycopg2
from connect import get_db_connection

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            connection = get_db_connection()

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM akun WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user is not None:
                request.session['username'] = user[0]
                return redirect('main')
            else:
                messages.error(request, 'Username or password is incorrect')
                return redirect('main:login')

        except psycopg2.Error as e:
            print(e)
            return HttpResponse("Error occurred while connecting to the database")

        finally:
            if connection:
                cursor.close()
                connection.close()

    else:
        return render(request, 'authentication/login.html')

def show_register_main(request):
    context = {
    }

    return render(request, "regist_main.html", context)

def show_register_pengguna(request):
    context = {
    }

    return render(request, "regist.html", context)

def show_dashboard_podcast(request):
    context = {
    }

    return render(request, "dashboard_podcast.html", context)

def show_register_label(request):
    context = {
    }

    return render(request, "regist_label.html", context)

def get_random_data():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM AKUN")
    akun = cursor.fetchall()
    
    print(akun)
    
    
get_random_data()