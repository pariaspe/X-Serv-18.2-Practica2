from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from .models import URLs

FORM = """
    <form action="" method="POST">
        <label for="url">URL a acrotar:</label><br>
        <input type="text" name="url" value="gsyc.es"/><br>
        <input type="submit" value="Send url">
    </form>
"""

def clean_url(url):
    if url.startswith('http') or url.startswith('https'):
        return url
    else:
        return 'http://' + url

@csrf_exempt
def barra(request):
    msg = ''
    if request.method == 'POST':
        print(request.POST['url'])
        url = URLs(url=clean_url(request.POST['url']))
        try:
            url.save()
            msg = 'URL añadida!'
        except IntegrityError:
            url = URLs.objects.get(url=url)
            msg = 'La URL ya ha sido añadida en: <a href=/' + str(url.id) + '>/' + str(url.id)  +'</a>'
    elif request.method == 'GET':
        pass
    else:
        return HttpResponse('<html><body>Metodo invalido:' + request.method + '</body></html>')

    lista = URLs.objects.all()
    respuesta = '<html><body><h1>Bienvenido al acortador de URLs:</h1>' + FORM
    respuesta += msg + '<h3>Lista de URLs acortadas:</h3>'
    for url in lista:
        respuesta += str(url.id) + ' ' + url.url + '<br>'
    respuesta += '</body></html>'
    return HttpResponse(respuesta)

def numero(request, numero):
    try:
        url = URLs.objects.get(id=str(numero))
        return HttpResponseRedirect(url)
    except URLs.DoesNotExist:
        return HttpResponse('<html><body>No existe este recurso acortado.</body></html>')
