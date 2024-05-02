from django.shortcuts import render

# Create your views here.
def show_detail_podcast(request):
    context = {
    }

    return render(request, "detail.html", context)

def show_chart(request):
    context = {
    }

    return render(request, "chart.html", context)

def show_chart_detail(request):
    context = {
    }

    return render(request, "chart_detail.html", context)

def create_podcast(request):
    context = {
    }

    return render(request, "create_podcast.html", context)

def show_podcast_list(request):
    context = {
    }

    return render(request, "podcast_list.html", context)

def show_create_episode(request):
    context = {
    }

    return render(request, "create_episode.html", context)

def show_episode_list(request):
    context = {
    }

    return render(request, "episode_list.html", context)