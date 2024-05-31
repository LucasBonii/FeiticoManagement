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
        produto_selecionado = Produto.objects.filter(id=id_produto).first()
        quantidade = request.POST.get("quantidade")
        print(quantidade)
        if quantidade:
            try:
                quantidade = int(quantidade)
                if produto_selecionado:
                    produto_selecionado.quantidade += quantidade
                    produto_selecionado.save()
                    quantidade = 0
                    mensagem = "sucesso"
                    return redirect('add_estoque', id_produto=id_produto)
                    
            except ValueError:
                mensagem = "número"
        selecionado = True

    if request.method == "POST" and not id_produto:  # Se o formulário for preenchido e id_produto não está na URL
        id_produto = request.POST.get("id_produto")
        if id_produto:
            return redirect('add_estoque', id_produto=id_produto)

    context = {"mensagem": mensagem, "selecionado": selecionado, "produto": produto_selecionado}
    return render(request, 'stock/pages/add_estoque.html', context)


def add_cliente(request):
    mensagem = None
    if request.method == "POST":
        dados = request.POST.dict()
        nome = dados.get("nome")
        cpf = dados.get("cpf")
        telefone = dados.get("telefone")

        cliente = Cliente.objects.filter(cli_cpf=cpf).first()
        if cliente:
            mensagem = "Erro"
        else:
            cliente = Cliente.objects.create(cli_nome=nome, cli_cpf=cpf, cli_telefone=telefone)
            mensagem = "Sucesso"

    context = {"mensagem": mensagem}
    return render(request, 'stock/pages/add_cliente.html', context)