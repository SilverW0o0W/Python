# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
import json
from info_collector import InfoCollector

collector = InfoCollector()


# Create your views here.
def index(request):
    context = {
    }
    return render(request, 'music/index.html', context)


def detail_action(request):
    url = request.POST.get('url', None)
    if not url:
        context = {
            'alert': "Url Invalid!",
        }
        return render(request, 'music/index.html', context)
    context = collector.request_url(url)
    if not context:
        pass
    return HttpResponse(json.dumps(context, ensure_ascii=False), content_type="application/json")
