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

        if Fornecedor.objects.filter(cnpj=cnpj).exists() or Fornecedor.objects.filter(nome_fornecedor=nome).exists():
            mensagem = "Erro"
        else:
            fornecedor = Fornecedor.objects.create(cnpj=cnpj, nome_fornecedor=nome)
            fornecedor.save()
            mensagem = "Sucesso"
    context = {"mensagem": mensagem}
    return render(request, 'stock/pages/add_fornecedor.html', context)


def add_produto(request):
    mensagem = None
    if request.method == "POST":            #Se o formulário for preenchido
        dados = request.POST.dict()
        fornecedor = dados.get("fornecedor")
        descricao = dados.get("descricao")
        valor = dados.get("valor")
        tamanho = dados.get("tamanho")
        cor = dados.get("cor")
        
        fornecedor = Fornecedor.objects.filter(id=fornecedor).first()
        if fornecedor:
            produto = Produto.objects.filter(fornecedor=fornecedor, descricao=descricao).first()
            if produto:
                mensagem = "Erro produto"
            else:
                produto = Produto.objects.create(fornecedor=fornecedor, descricao=descricao, valor=valor, tamanho=tamanho, cor=cor)
                produto.save()
                mensagem = "Sucesso"
        else:
            mensagem = "Erro Fornecedor"
    context = {"mensagem": mensagem}
    return render(request, 'stock/pages/add_produto.html', context)