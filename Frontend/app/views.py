from django.shortcuts import render
from app.forms import RangoForm
import requests

# Create your views here.

endpoint = 'http://localhost:3000/'
def home(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    
    elif request.method == 'POST':
        docs = request.FILES['archivo_entrada']
        data = docs.read()
        response = requests.post(endpoint + 'agregar_solicitud', data)
        respuesta = response.json()
        context = {
            'respuesta' : respuesta
        }
        return render(request, 'index.html', context)

def rango(request):
    return render(request, 'rango.html')

def resumen_iva(request):
    return render(request, 'resumen_iva.html')

'''
def rango(request):
    if request.method == "POST":
        form = RangoForm(request.POST)
        if form.is_valid():
            json_data = form.cleaned_data
            response = requests.post(endpoint + 'rango', json=json_data)
            contenido = response.json()
            context = {
            'contenido' : contenido
            }
            return render(request, 'rango.html', context)
        return render(request, 'rango.html', {'form':form})
    return render(request, 'rango.html')
'''
