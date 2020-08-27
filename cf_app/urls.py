from django.urls import path
from . import views

urlpatterns = [
    # /cf/test/
    path('test/', views.test_api),
    path('es-list/', views.test_es_list_api),
    path('es-index-list/', views.test_es_get_all_api),
]
