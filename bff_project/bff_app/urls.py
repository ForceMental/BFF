from . import views
from django.urls import path
from .views import get_all_client, insertar_persona, get_user_view, get_visitas_by_date, crear_visita, enviar_datos_a_ventas, get_all_product, get_all_comunas, reprogramar_serv, cancelar_visita,finalizar_visita

urlpatterns = [
    path('comunas/', get_all_comunas, name='comunas'),
    path('clientes/', get_all_client, name='client'),
    path('ingreso_clientes/', insertar_persona, name='set-client'),
    path('view_users/', get_user_view, name='view_users'),
    path('visitas/<str:fecha>', get_visitas_by_date, name='visitas'),
    path('visitas-crear/', crear_visita, name='visitas-crear'),
    path('view_all/', views.view_all_users, name='view_all_users'),
    path('productos/', views.get_all_product, name='client'),
    path('visitasIdFecha/', views.get_visitas_by_date_id, name='visitas-id-fecha'),
    path('reprogramar-visita/<int:pk>/', views.reprogramar_serv, name='reprogramar_visita'),
    path('cancelar/<int:pk>/', views.cancelar_visita, name='cancelar'),
    path('finalizar/<int:pk>/', views.finalizar_visita, name='finalizar'),
    path('ventas/', views.enviar_datos_a_ventas, name='ventas')

]
