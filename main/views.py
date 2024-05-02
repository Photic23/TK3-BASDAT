from django.shortcuts import render

# Create your views here.

def show_register(request):
    context = {
    }

    return render(request, "regist.html", context)