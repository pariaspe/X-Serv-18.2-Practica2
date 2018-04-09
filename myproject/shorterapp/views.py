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
        return url.replace('%3A%2F%2F', '://')
    else:
        return 'http://' + url

@csrf_exempt
def barra(request):
    if request.method == 'POST':
        print(request.POST['url'])
        url = URLs(url=request.POST['url'])
        try:
            url.save()
            return HttpResponse('URL añadida!')
        except IntegrityError:
            return HttpResponse('La URL ya ha sido añadida')

    elif request.method == 'GET':
        lista = URLs.objects.all()
        respuesta = '<h1>Bienvenido al acortador de URLs:</h1>' + FORM
        respuesta += '<h3>Lista de URLs acortadas:</h3>'
        for url in lista:
            respuesta += str(url.id) + ' ' + url.url + '<br>'
        return HttpResponse(respuesta)
    else:
        return HttpResponse('Metodo invalido:' + request.method)

def numero(request, numero):
    try:
        url = URLs.objects.get(id=str(numero))
        return HttpResponseRedirect(url)
    except URLs.DoesNotExist:
        return HttpResponse('No existe pagina')
