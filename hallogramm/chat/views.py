from django.http import HttpResponse
from django.shortcuts import render


def show_chat(request):
    return HttpResponse('<h1>ЗБС<h1>')