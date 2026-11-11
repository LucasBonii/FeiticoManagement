from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PostgresLoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.db.models import Sum
from .models import *
from datetime import datetime
from .utils import *


def home(request):
    usuario = None
    verificar_cadastro(request)
    usuario = Funcionario.objects.get(usuario=request.session['postgres_user'])
    if not usuario:
        return redirect('completar_cadastro')
    
    vendas = Venda.objects.filter(finalizada=True).order_by("-horario")[:10]

    produtos_top = ItensPedido.objects.values('produto__descricao').annotate(quantidade=Sum('quantidade'), preco_total=Sum('preco_parcial')).order_by('-quantidade')[:10]
    context = {"vendas": vendas, "produtos": produtos_top}
    return render(request, 'stock/pages/home.html', context)


@require_access_level(['Gerente', 'Estoquista'])
def add_fornecedor(request):
    mensagem = None
    usuario = None
    verificar_cadastro(request)
    usuario = Funcionario.objects.get(usuario=request.session['postgres_user'])
    if not usuario:
        return redirect('completar_cadastro')
    
    if request.method == "POST":            
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


@require_access_level(['Gerente', 'Estoquista'])
def add_produto(request):
    mensagem = None
    usuario = None
    verificar_cadastro(request)
    usuario = Funcionario.objects.get(usuario=request.session['postgres_user'])
    if not usuario:
        return redirect('completar_cadastro')
    
    if request.method == "POST":            
        dados = request.POST.dict()
        fornecedor = dados.get("fornecedor")
        descricao = dados.get("descricao")
        valor = dados.get("valor")
        tamanho = dados.get("tamanho")
        cor = dados.get("cor")
        
        fornecedor = Fornecedor.objects.filter(id=fornecedor).first()
        if fornecedor:
            produto = Produto.objects.filter(fornecedor=fornecedor, descricao=descricao, tamanho=tamanho, cor=cor).first()
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


@require_access_level(['Gerente', 'Estoquista'])
def add_estoque(request, id_produto=None):
    mensagem = None
    selecionado = False
    produto_selecionado = None
    usuario = None
    verificar_cadastro(request)
    usuario = Funcionario.objects.get(usuario=request.session['postgres_user'])
    if not usuario:
        return redirect('completar_cadastro')

    if id_produto:  # Se o ID do produto estiver presente na URL
        produto_selecionado = Produto.objects.filter(id=id_produto).first()
        quantidade = request.POST.get("quantidade")
        if quantidade:
            try:
                quantidade = int(quantidade)
                if produto_selecionado:
                    if (produto_selecionado.quantidade + quantidade) >= 0:
                        produto_selecionado.quantidade += quantidade
                        produto_selecionado.save()
                        quantidade = 0
                        mensagem = "sucesso"
                        return redirect('add_estoque', id_produto=id_produto)
                    
            except ValueError:
                mensagem = "número"
        selecionado = True

    if request.method == "POST" and not id_produto:
        id_produto = request.POST.get("id_produto")
        if id_produto:
            return redirect('add_estoque', id_produto=id_produto)

    context = {"mensagem": mensagem, "selecionado": selecionado, "produto": produto_selecionado}
    return render(request, 'stock/pages/add_estoque.html', context)


@require_access_level(['Gerente', 'Vendedor'])
def add_cliente(request):
    mensagem = None
    usuario = None
    verificar_cadastro(request)
    usuario = Funcionario.objects.get(usuario=request.session['postgres_user'])
    if not usuario:
        return redirect('completar_cadastro')
    if request.method == "POST":
        dados = request.POST.dict()
        nome = dados.get("nome")
        cpf = dados.get("cpf")
        telefone = dados.get("telefone")

        cliente = Cliente.objects.filter(cpf=cpf).first()
        if cliente:
            mensagem = "Erro"
        else:
            cliente = Cliente.objects.create(nome=nome, cpf=cpf, telefone=telefone)
            mensagem = "Sucesso"

    context = {"mensagem": mensagem}
    return render(request, 'stock/pages/add_cliente.html', context)


@require_access_level(['Gerente'])
def add_funcionario(request):
    mensagem = None
    usuario = None
    verificar_cadastro(request)
    usuario = Funcionario.objects.get(usuario=request.session['postgres_user'])
    if not usuario:
        return redirect('completar_cadastro')
    
    cargos = Cargo.objects.all()

    if request.method == "POST":
        dados = request.POST.dict()
        if "cpf" in dados and "senha" in dados and "nome" in dados and "cargo" in dados and "telefone" in dados:
            cpf = dados.get("cpf")
            senha = dados.get("senha")
            id_cargo = dados.get("cargo")
            telefone = dados.get("telefone")
            nome = dados.get("nome")

            username = nome.replace(" ", "")
            username = username.lower()

            cargo = Cargo.objects.get(id=id_cargo)
            funcionario = Funcionario.objects.create(
                cpf=cpf,
                nome=nome,
                telefone=telefone,
                funcao=cargo,
                usuario=username
            )
            criar_usuario_postgre(nome, senha, cargo.cargo)   
            mensagem = "Sucesso"
            

        else:
            mensagem = "Erro Informaçoes"

    context = {"mensagem": mensagem, "cargos": cargos}
    return render(request, 'stock/pages/add_funcionario.html', context)



@require_access_level(['Gerente', 'Vendedor'])
def add_venda(request):
    itens_venda = None
    usuario = None
    verificar_cadastro(request)
    usuario = Funcionario.objects.get(usuario=request.session['postgres_user'])
    if not usuario:
        return redirect('completar_cadastro')
    
    venda, criado = Venda.objects.get_or_create(funcionario=usuario, finalizada=False)
    venda.valor_total = calcular_preco_total(venda)
    venda.save()
    itens_venda = ItensPedido.objects.filter(pedido=venda)
    cliente = venda.cliente
    if request.method == "POST":
        dados = request.POST.dict()
        quantidade = dados.get("quantidade")
        codigo = dados.get("codigo")
        cpf_cliente = dados.get("cliente")
        if codigo and quantidade:
            if cpf_cliente:
                cliente = Cliente.objects.get(cpf=cpf_cliente)
                if cliente:
                    venda.cliente = cliente
                    venda.save()

            quantidade = int(quantidade)
            produto = Produto.objects.get(id=codigo)
            if produto and produto.quantidade >= quantidade:
                item_pedido, criado = ItensPedido.objects.get_or_create(produto=produto, pedido=venda)
                
                if produto.quantidade >= (item_pedido.quantidade + quantidade):
                    item_pedido.quantidade += quantidade
                    item_pedido.preco_parcial = calcular_preco_parcial(item_pedido)
                    item_pedido.save()
                    return redirect('add_venda')

                
        cpf_cliente = dados.get("cliente")
        if cpf_cliente:
            cliente = Cliente.objects.get(cpf=cpf_cliente)
            if cliente:
                venda.cliente = cliente
                venda.save()
            #venda.valor_total = 

    context = {"itens":itens_venda, "cliente": cliente, "venda": venda}
    return render(request, 'stock/pages/add_venda.html', context)
    


@require_access_level(['Gerente', 'Vendedor'])
def finalizar_venda(request):
    usuario = None
    verificar_cadastro(request)
    usuario = Funcionario.objects.get(usuario=request.session['postgres_user'])
    if not usuario:
        return redirect('completar_cadastro')
    
    venda, criado = Venda.objects.get_or_create(funcionario=usuario, finalizada=False)
    verificado = verificar_quantidades(venda)
    if verificado:
        diminuir_estoque(venda)
        venda.finalizada = True
        venda.horario = datetime.now()
        venda.save()
    return redirect('add_venda')


@require_access_level(['Gerente', 'Vendedor'])
def cancelar_venda(request):
    usuario = None
    verificar_cadastro(request)
    usuario = Funcionario.objects.get(usuario=request.session['postgres_user'])
    if not usuario:
        return redirect('completar_cadastro')
    
    venda, criado = Venda.objects.get_or_create(funcionario=usuario, finalizada=False)
    venda.delete()
    return redirect('add_venda')



def completar_cadastro(request):
    usuario = request.session['postgres_user']
    if request.method == "POST":
        dados = request.POST.dict()
        nome = dados.get("nome")
        cpf = dados.get("cpf")
        telefone = dados.get("telefone")
        senha = dados.get("senha")
        
        fazer_login_postgre(request, username=request.session['postgres_sql'])
        
        funcionario, criado = Funcionario.objects.get_or_create(cpf=cpf)
        if not criado:
            return redirect('completar_cadastro')
        elif criado:
            funcionario.usuario = usuario
            funcionario.nome = nome
            funcionario.telefone = telefone
            criar_usuario_postgre(nome, senha, 'gerente')
            funcionario.save()
            
            return redirect('home')

    return render(request, 'stock/pages/completar_cadastro.html')


def fazer_logout(request):
    request.session.pop('postgres_user', None)
    return redirect("fazer_login")


def fazer_login(request):
    if request.method == 'POST':
        username = request.POST.get('nome')
        password = request.POST.get('senha')
        username = username.replace(" ", "")
        username = username.lower()
        fazer_login_postgre(request, username, password)
        return redirect('home') 
    return render(request, 'stock/pages/fazer_login.html')


@require_access_level(['Gerente', 'Analista'])
def exportar_relatorio(request, relatorio):
    usuario = None
    verificar_cadastro(request)
    usuario = Funcionario.objects.get(usuario=request.session['postgres_user'])
    if not usuario:
        return redirect('completar_cadastro')
    if relatorio == "venda":
        informacoes = Venda.objects.filter(finalizada=True)
    elif relatorio == "cliente":
        informacoes = Cliente.objects.all()
    elif relatorio == "funcionario":
        informacoes = Funcionario.objects.all()
    elif relatorio == "itens":
        informacoes = ItensPedido.objects.filter(pedido__finalizada=True)
    return exportar_csv(informacoes)