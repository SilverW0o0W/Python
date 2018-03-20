# coding=utf-8
from django.shortcuts import render
from django.http import FileResponse

from lyric_exporter import LyricExporter


# Create your views here.

def index(request):
    context = {
    }
    return render(request, 'lyric_exporter/index.html', context)


download_path = 'lyric_exporter/download'
lyric_dir = str.format('{0}/lyric/', download_path)
playlist_dir = str.format('{0}/playlist/', download_path)


def export_action(request):
    url = request.POST.get('id', None)
    if not url:
        context = {
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
    file_name = exporter.get_song(url) if url_type == 'song' else exporter.get_playlist(url, playlist_dir)
    file_stream = open(file_name[1], 'rb')
    response = FileResponse(file_stream)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = str.format('attachment;filename={0}', file_name[0])
    return response


def export_music_action(request):
    pass


def export_playlist_action(request):
    pass
