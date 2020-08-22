from django.urls import path
from . import views

urlpatterns = [
    # /cf/test/
    path('test/', views.test_api)
]
