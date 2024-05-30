from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def home(request):
    return render(request, 'stock/pages/home.html')


def add_fornecedor(request):
    mensagem = None
    if request.method == "POST":            #Se o formulário for preenchido
        dados = request.POST.dict()
        cnpj = dados.get("cnpj")
        nome = dados.get("nome")
        fornecedor, criado = Fornecedor.objects.get_or_create(cnpj=cnpj, nome_fornecedor=nome)
        if criado == False:
            mensagem = "Erro"
        else:
            mensagem = "Sucesso"
    context = {"mensagem": mensagem}
    return render(request, 'stock/pages/add_fornecedor.html', context)