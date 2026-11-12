from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('control/img/logo.ico'))),
    path('ingresar/', views.ingresar, name='login'),
    path('registro/', views.registro, name='registro'),
    path('salir/', views.salir, name='salir'),
    path('reportes/<str:tipo>/', views.reporte, name='reporte'),
    path('<str:seccion>/', views.listado, name='listado'),
    path('<str:seccion>/nuevo/', views.guardar, name='nuevo'),
    path('<str:seccion>/editar/<int:pk>/', views.guardar, name='editar'),
    path('<str:seccion>/eliminar/<int:pk>/', views.eliminar, name='eliminar'),
    path('<str:seccion>/imprimir/<int:pk>/', views.imprimir, name='imprimir'),
]