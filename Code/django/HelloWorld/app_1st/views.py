from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.


def index(request):
    template = loader.get_template('polls/index.html')
    return HttpResponse("Hello app.")


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
