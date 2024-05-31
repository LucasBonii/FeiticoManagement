from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('fornecedor/', views.add_fornecedor, name="add_fornecedor"),
    path('produto/', views.add_produto, name="add_produto"),
    path('estoque/', views.add_estoque, name="add_estoque"),
    path('estoque/<int:id_produto>', views.add_estoque, name="add_estoque"),
    path('cliente/', views.add_cliente, name="add_cliente"),
    path('funcionario/', views.add_funcionario, name="add_funcionario"),
    #path('funcionario/', views.fazer_login, name="fazer_login"),
]