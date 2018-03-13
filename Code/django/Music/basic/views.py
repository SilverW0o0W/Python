# coding=utf-8
from django.shortcuts import render
from info_collector import InfoCollector

collector = InfoCollector()


# Create your views here.
def index(request):
    context = {
    }
    return render(request, 'music/index.html', context)


def display_action(request):
    url = request.POST.get('url', None)
    if not url:
        context = {
            'alert': "Url Invalid!",
        }
        return render(request, 'music/index.html', context)
    context = collector.request_song(url) if type == 'song' else collector.request_playlist(url)
    context['display'] = True
    context['type'] = type
    return render(request, 'music/index.html', context)
