from . import views
from django.urls import path
from .views import get_all_client, insertar_persona, get_user_view, get_visitas_by_date, crear_visita, get_all_product, get_all_comunas

urlpatterns = [
    path('comunas/', get_all_comunas, name='comunas'),
    path('clientes/', get_all_client, name='client'),
    path('ingreso_clientes/', insertar_persona, name='set-client'),
    path('view_users/', get_user_view, name='view_users'),
    path('visitas/<str:fecha>', get_visitas_by_date, name='visitas'),
    path('visitas-crear/', crear_visita, name='visitas-crear'),
    path('view_all/', views.view_all_users, name='view_all_users'),
    path('productos/', get_all_product, name='client'),
]
