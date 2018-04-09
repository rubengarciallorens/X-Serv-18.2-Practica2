# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import URL

# Create your views here.

@csrf_exempt
def barra(request):
    if request.method == "GET":
        # Imprimir la base de datos
        answer = "Saved URLs" 
        URL_list = URL.objects.all()
        for url in URL_list:
            answer += "<br>" + url.name + " --> Id = " + str(url.id)
        # Introducir nuevas en base de datos
        answer += "<br>New url:<br>"
        answer += "<form action='/' method='post'>"
        answer += "Name: <input type= 'text' name='name'>"
        answer += "<input type= 'submit' value='SEND'>"
        answer += "</form>"
        sts = 200
    elif request.method == "POST":
        name = request.POST['name']  # URL que intenta guardar
        if name.startswith('http://') or name.startswith('https://'):
            url_Guard = name
            answer = "Page = " + url_Guard
        else:
            url_Guard = "http://" + name
            answer = "Page = " + url_Guard
        try:
            url_busq = URL.objects.get(name=url_Guard)
            answer += "<br>URL already exists "
            answer += ("<a href=" + url_busq.name + ">localhost:1234/" +
                          str(url_busq.id) + "</a>")
        except URL.DoesNotExist:
            answer += "<br> Saved in database"
            url_def = URL(name=url_Guard)
            url_def.save()

        sts = 200
    else:
        answer = "Method Not Allowed"
        sts = 405
    return HttpResponse(answer, status=sts)


def busqURL(request, identificador):
    if request.method == "GET":
        try:
            url_busq = URL.objects.get(id=identificador)
            answer = "Page already saved "
            return redirect(url_busq.name)
        except URL.DoesNotExist:
            answer = "<br> Page doesn't exist"
            sts = 404
    else:
        answer = "Method Not Allowed"
        sts = 405

    return HttpResponse(answer, status=sts)