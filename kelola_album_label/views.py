from django.shortcuts import render

# Create your views here.
def show_list_album(request):
    context = {
    }

    return render(request, "list_album_label.html", context)

def show_list_lagu(request):
    context = {
    }

    return render(request, "list_lagu_label.html", context)