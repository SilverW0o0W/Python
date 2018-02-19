from django.shortcuts import render
from django.http import FileResponse

from models import Lyric
from lyric_exporter import LyricExporter
import spider.music_utils as utils


# Create your views here.


def index(request):
    context = {
        'welcome': "First Page of App Lyric Exporter",
    }
    return render(request, 'lyric_exporter/index.html', context)


def export_action(request):
    url = request.POST.get('url', None)
    if not url:
        context = {
            'welcome': "First Page of App Lyric Exporter",
        }
        return render(request, 'lyric_exporter/index.html', context)
    type = request.POST.get('type', 'song')
    format = request.POST.get('format', '1')
    format_dict = {
        '1': '{1}',
        '2': '{0} - {1}',
        '3': '{1} - {0}',
    }
    name_format = format_dict[format]
    exporter = LyricExporter('lyric_exporter/download/lyric/', name_format=name_format)
    path = export_song(exporter, url) if type == 'song' else export_playlist(exporter, url)
    file = open(path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="test.lrc'
    return response


def export_song(exporter, url):
    song_id = utils.match_song_id(url)
    path = exporter.export(song_id)
    lyric = Lyric()
    lyric.song_id = id
    lyric.locate_path = path
    lyric.save()
    return path


def export_playlist(exporter, url):
    playlist_id = utils.match_playlist_id(url)
    path_dict = exporter.export_playlist(playlist_id)
    for path in path_dict:
        lyric = Lyric()
        lyric.song_id = path
        lyric.locate_path = path
        lyric.save()