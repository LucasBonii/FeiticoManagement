from django.urls import path
from . import views

urlpatterns = [
    path('', views.fazer_login, name="fazer_login"),
    path('home/', views.home, name="home"),
    path('fornecedor/', views.add_fornecedor, name="add_fornecedor"),
    path('produto/', views.add_produto, name="add_produto"),
    path('estoque/', views.add_estoque, name="add_estoque"),
    path('estoque/<int:id_produto>', views.add_estoque, name="add_estoque"),
    path('cliente/', views.add_cliente, name="add_cliente"),
    path('funcionario/', views.add_funcionario, name="add_funcionario"),
    path('venda/', views.add_venda, name="add_venda"),
    path('finalizar_venda/', views.finalizar_venda, name="finalizar_venda"),
    path('cancelar_venda/', views.cancelar_venda, name="cancelar_venda"),
    path('logout/', views.fazer_logout, name='fazer_logout'),
    path('completarcadastro/', views.completar_cadastro, name='completar_cadastro'),
    path('exportar_relatorio/<str:relatorio>', views.exportar_relatorio, name="exportar_relatorio"),
]