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
            msg = 'La URL ya ha sido añadida en: <a href=/' + str(url.id)
            msg += '>/' + str(url.id) + '</a>'
    elif request.method == 'GET':
        pass
    else:
        respuesta = '<html><body>Metodo invalido:' + request.method
        respuesta += '</body></html>'
        return HttpResponse(respuesta)

    lista = URLs.objects.all()
    respuesta = '<html><body><h1>Bienvenido al acortador de URLs:</h1>' + FORM
    respuesta += msg + '<h3>Lista de URLs acortadas:</h3><ul>'
    for url in lista:
        respuesta += '<li><a href=/' + str(url.id) + '>/' + str(url.id)
        respuesta += '</a>. ' + url.url + '<br>'
    respuesta += '</lul</body></html>'
    return HttpResponse(respuesta)


def numero(request, numero):
    try:
        url = URLs.objects.get(id=str(numero))
        return HttpResponseRedirect(url)
    except URLs.DoesNotExist:
        respuesta = '<html><body>No existe el recurso acortado.</body></html>'
        return HttpResponse(respuesta)
