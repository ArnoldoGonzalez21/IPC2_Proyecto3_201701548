from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'index'),
    path('rango/', views.rango, name = 'rango'),
    path('resumen_iva/', views.resumen_iva, name = 'resumen_iva'),
    path('documentacion/', views.pdf_view, name = 'documentacion'),

]