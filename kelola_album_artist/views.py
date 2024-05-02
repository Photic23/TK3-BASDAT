from django.shortcuts import render

# Create your views here.

def show_create_album(request):
    context = {
    }

    return render(request, "create_album.html", context)

def show_create_lagu(request):
    context = {
    }

    return render(request, "create_lagu_artist.html", context)

def show_create_lagu_songwriter(request):
    context = {
    }

    return render(request, "create_lagu_songwriter.html", context)


def show_list_album(request):
    context = {
    }

    return render(request, "list_album.html", context)

def show_list_lagu(request):
    context = {
    }

    return render(request, "list_lagu.html", context)