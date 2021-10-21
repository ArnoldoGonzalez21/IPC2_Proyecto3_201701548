from django.shortcuts import render
import requests

# Create your views here.

endpoint = 'http://localhost:3000/'
def home(request):
    if request.method == 'GET':
        response = requests.get(endpoint + 'mostrar_solicitudes')
        solicitudes = response.json()
        context = {
            'solicitudes' : solicitudes
        }
        return render(request, 'index.html', context)
    elif request.method == 'POST':
        docs = request.FILES['archivo_entrada']
        data = docs.read()
        response = requests.post(endpoint + 'agregar_solicitud', data)
        respuesta = response.json()
        context = {
            'respuesta' : respuesta
        }
        return render(request, 'index.html', context)