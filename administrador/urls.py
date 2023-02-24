from django.urls import path

from .views import home, galileo_home, crear_sitio, leer_sitio, \
    editar_sitio, eliminar_sitio, genesis, galileo, galileo_home, genesis_home, sign_in, \
        crear_reserva, leer_reserva, editar_reserva, eliminar_reserva, lista_control

urlpatterns = [
    path('', home, name="home"),
    path('sign_in/', sign_in, name='sign_in'),
    path('genesis/', genesis, name='genesis'),
    path('galileo/', galileo, name='galileo'),
    path('galileo_home/', galileo_home, name='galileo_home'),
    path('genesis_home/', genesis_home, name='genesis_home'),
    path('crear_sitio/', crear_sitio, name='crear_sitio'),
    path('leer_sitio/', leer_sitio, name='leer_sitio'),
    path('editar_sitio/<id>/', editar_sitio, name='editar_sitio'),
    path('eliminar_sitio/<id>/', eliminar_sitio, name='eliminar_sitio'),
    path('crear_reserva/', crear_reserva, name='crear_reserva'),
    path('leer_reserva/', leer_reserva, name='leer_reserva'),
    path('editar_reserva/<id>/', editar_reserva, name='editar_reserva'),
    path('eliminar_reserva/<id>/', eliminar_reserva, name='eliminar_reserva'),
    path('lista_control/', lista_control, name='lista_control'),
    

]
