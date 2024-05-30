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


def add_estoque(request, id_produto=None):
    mensagem = None
    selecionado = False
    produto_selecionado = None
    
    if id_produto:  # Se o ID do produto estiver presente na URL
        selecionado = True
        produto_selecionado = Produto.objects.filter(id=id_produto).first()

    if request.method == "POST":  # Se o formulário for preenchido
        id_produto = request.POST.get("id_produto")
        if id_produto:
            return redirect('add_estoque', id_produto=id_produto)
    
    context = {"mensagem": mensagem, "selecionado": selecionado, "produto": produto_selecionado}
    return render(request, 'stock/pages/add_estoque.html', context)