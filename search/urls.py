from django.urls import path
from . import views

urlpatterns = [
    # /search/test/
    path('test/', views.test_api),
]