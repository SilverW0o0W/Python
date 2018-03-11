# coding=utf-8
from django.shortcuts import render
from spider.music_spider import MusicSpider

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
    url_type = request.POST.get('type', 'song')
    # file_name = display_song(exporter, url) if url_type == 'song' else export_playlist(exporter, url)
    return render(request, 'music/index.html')
