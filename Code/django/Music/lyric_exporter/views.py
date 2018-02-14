from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    context = {
        'welcome': "First Page of App Lyric Exporter",
    }
    return render(request, 'lyric_exporter/index.html', context)

def export(request):
    return render(request,'lyric_exporter/index.html')