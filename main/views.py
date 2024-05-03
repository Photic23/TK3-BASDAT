from django.shortcuts import render

# Create your views here.

def show_register_main(request):
    context = {
    }

    return render(request, "regist_main.html", context)

def show_register_pegguna(request):
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