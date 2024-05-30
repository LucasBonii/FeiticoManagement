from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('fornecedor/', views.add_fornecedor, name="add_fornecedor"),
]