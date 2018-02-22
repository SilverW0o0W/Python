# coding=utf-8
from django.shortcuts import render
from django.http import FileResponse

from models import Lyric
from lyric_exporter import LyricExporter
import spider.music_utils as utils
import zipfile
import os


# Create your views here.

def index(request):
    context = {
        'welcome': "First Page of App Lyric Exporter",
    }
    return render(request, 'lyric_exporter/index.html', context)


download_path = 'lyric_exporter/download'


def export_action(request):
    url = request.POST.get('url', None)
    if not url:
        context = {
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
    lyric_dir = str.format('{0}/lyric/', download_path)
    exporter = LyricExporter(lyric_dir, name_format=name_format)
    file_name = export_song(exporter, url) if url_type == 'song' else export_playlist(exporter, url)
    file = open(file_name[1], 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = str.format('attachment;filename={0}', file_name[0])
    return response


def export_song(exporter, url):
    song_id = utils.match_song_id(url)
    # try:
    #     lyric = Lyric.objects.get(song_id=song_id)
    #     locate_path = lyric.locate_path
    # except Lyric.DoesNotExist:
    #     locate_path = None
    # locate_path = lyric.locate_path
    file_name = exporter.export(song_id)
    lyric = Lyric()
    lyric.song_id = song_id
    lyric.file_name = file_name[0]
    lyric.locate_path = file_name[1]
    lyric.save()
    return file_name


def export_playlist(exporter, url):
    playlist_id = utils.match_playlist_id(url)
    path_dict = exporter.export_playlist(playlist_id)
    zip_name = str.format('{0}.zip', playlist_id)
    playlist_dir = str.format('{0}/playlist', download_path)
    zip_real_name = str.format('{0}/{1}', playlist_dir, zip_name)

    if not os.path.isdir(playlist_dir):
        os.makedirs(playlist_dir)

    with zipfile.ZipFile(zip_real_name, 'w') as zip_file:
        for song_id, file_name in path_dict.items():
            lyric = Lyric()
            lyric.song_id = song_id
            lyric.file_name = file_name[0]
            lyric.locate_path = file_name[1]
            lyric.save()
            short_name = file_name[0].decode('utf-8')
            long_name = file_name[1].decode('utf-8')
            zip_file.write(long_name, short_name, compress_type=zipfile.ZIP_DEFLATED)
    return zip_name, zip_real_name
