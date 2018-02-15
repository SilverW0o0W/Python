from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def index(request):
    context = {
        'welcome': "First Page of App Lyric Exporter",
    }
    return render(request, 'lyric_exporter/index.html', context)


def export_action(request):
    type = request.POST.get('type', 'song')
    url = request.POST.get('song_url', None)
    context = {
        'welcome': url,
    }
    return render(request, 'lyric_exporter/index.html', context)
