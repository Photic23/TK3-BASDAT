from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
    }

    return render(request, "list_royalti.html", context)