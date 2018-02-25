# coding=utf-8
from django.shortcuts import render
from django.http import FileResponse

from lyric_exporter import LyricExporter
import spider.music_utils as utils


# Create your views here.

def index(request):
    context = {
        'welcome': "First Page of App Lyric Exporter",
    }
    return render(request, 'lyric_exporter/index.html', context)


download_path = 'lyric_exporter/download'
lyric_dir = str.format('{0}/lyric/', download_path)
playlist_dir = str.format('{0}/playlist/', download_path)


def export_action(request):
    url = request.POST.get('url', None)
    if not url:
        context = {
            'alert': "Url Invalid!",
            'welcome': "First Page of App Lyric Exporter",
        }
        return render(request, 'lyric_exporter/index.html', context)
    url_type = request.POST.get('type', 'song')
    format = request.POST.get('format', '1')
    format_dict = {
        '1': '{1}',
        '2': '{0} - {1}',
        '3': '{1} - {0}',
    }
    name_format = format_dict[format]
    exporter = LyricExporter(lyric_dir, name_format=name_format)
    file_name = export_song(exporter, url) if url_type == 'song' else export_playlist(exporter, url)
    file_stream = open(file_name[1], 'rb')
    response = FileResponse(file_stream)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = str.format('attachment;filename={0}', file_name[0])
    return response


def export_song(exporter, url):
    song_id = utils.match_song_id(url)
    return exporter.export(song_id)


def export_playlist(exporter, url):
    playlist_id = utils.match_playlist_id(url)
    return exporter.export_playlist(playlist_id, playlist_dir=playlist_dir)
