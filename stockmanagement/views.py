from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.db.models import Sum
from .models import *
from datetime import datetime
from .utils import *


@login_required
def home(request):
    try:
        vendedor = request.user.funcionario
    except:
        return redirect('completar_cadastro')
    vendas = Venda.objects.filter(finalizada=True).order_by("-horario")[:10]

    produtos_top = ItensPedido.objects.values('produto__descricao').annotate(quantidade=Sum('quantidade'), preco_total=Sum('preco_parcial'))
    produtos_top.order_by('-quantidade')[:10]

    print(produtos_top)
    context = {"vendas": vendas, "produtos": produtos_top}
    return render(request, 'stock/pages/home.html', context)


@login_required
@user_passes_test(is_gerente_ou_estoquista,  login_url='/home/')
def add_fornecedor(request):
    try:
        vendedor = request.user.funcionario
    except:
        return redirect('completar_cadastro')
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


@login_required
@user_passes_test(is_gerente_ou_estoquista,  login_url='/home/')
def add_produto(request):
    try:
        vendedor = request.user.funcionario
    except:
        return redirect('completar_cadastro')
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


@login_required
@user_passes_test(is_gerente_ou_estoquista,  login_url='/home/')
def add_estoque(request, id_produto=None):
    try:
        vendedor = request.user.funcionario
    except:
        return redirect('completar_cadastro')
    mensagem = None
    selecionado = False
    produto_selecionado = None

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


@login_required
@user_passes_test(is_gerente_ou_vendedor,  login_url='/home/')
def add_cliente(request):
    try:
        vendedor = request.user.funcionario
    except:
        return redirect('completar_cadastro')
    mensagem = None
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


@login_required
@user_passes_test(lambda user: user.groups.filter(name='Gerente').exists(),  login_url='/home/')
def add_funcionario(request):
    try:
        vendedor = request.user.funcionario
    except:
        return redirect('completar_cadastro')
    mensagem = None
    cargos = Cargo.objects.all()

    if request.method == "POST":
        dados = request.POST.dict()
        if "cpf" in dados and "senha" in dados and "nome" in dados and "cargo" in dados and "telefone" in dados:
            cpf = dados.get("cpf")
            senha = dados.get("senha")
            id_cargo = dados.get("cargo")
            telefone = dados.get("telefone")
            nome = dados.get("nome")
       
            usuario, criado = User.objects.get_or_create(username=cpf)
            if criado:
                usuario.set_password(senha)
                usuario.save()
                cargo = Cargo.objects.get(id=id_cargo)
                funcionario = Funcionario.objects.create(
                    cpf=cpf,
                    nome=nome,
                    telefone=telefone,
                    funcao=cargo,
                    usuario=usuario
                )
                criar_usuario_postgre(nome, senha, cargo.cargo)
                grupo = Group.objects.get(name=cargo.cargo)  # Obtenha o grupo desejado pelo nome
                usuario.groups.add(grupo)
                if cargo.cargo == 'Gerente':
                    usuario.is_staff = True
                usuario.save()
                mensagem = "Sucesso"
            else:
                mensagem = "Erro"

        else:
            mensagem = "Erro Informaçoes"

    context = {"mensagem": mensagem, "cargos": cargos}
    return render(request, 'stock/pages/add_funcionario.html', context)


def fazer_login(request, login_url='/home/'):
    mensagem = None
    if request.user.is_authenticated:

        return redirect('add_funcionario')
    if request.method == "POST":
        dados = request.POST.dict()
        if "cpf" in dados and "senha" in dados:
            cpf = dados.get("cpf")
            senha = dados.get("senha")
            usuario = authenticate(request, username=cpf, password=senha)
            if usuario.funcionario.ativo:
                if usuario:
                    login(request, usuario)

                    return redirect('home')
                else:
                    mensagem= "Credenciais"
        else:
            mensagem = "Erro"

    context = {"mensagem": mensagem}
    return render(request, 'stock/pages/fazer_login.html', context)


@login_required
@user_passes_test(is_gerente_ou_vendedor,  login_url='/home/')
def add_venda(request):
    itens_venda = None
    try:
        vendedor = request.user.funcionario
    except:
        return redirect('completar_cadastro')
    venda, criado = Venda.objects.get_or_create(funcionario=vendedor, finalizada=False)
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
    

@login_required
@user_passes_test(is_gerente_ou_vendedor,  login_url='/home/')
def finalizar_venda(request):
    vendedor = request.user.funcionario
    venda, criado = Venda.objects.get_or_create(funcionario=vendedor, finalizada=False)
    verificado = verificar_quantidades(venda)
    if verificado:
        diminuir_estoque(venda)
        venda.finalizada = True
        venda.horario = datetime.now()
        venda.save()
    return redirect('add_venda')

@login_required
@user_passes_test(is_gerente_ou_vendedor,  login_url='/home/')
def cancelar_venda(request):
    try:
        vendedor = request.user.funcionario
    except:
        return redirect('completar_cadastro')
    vendedor = request.user.funcionario
    venda, criado = Venda.objects.get_or_create(funcionario=vendedor, finalizada=False)
    venda.delete()
    return redirect('add_venda')


@login_required
def completar_cadastro(request):
    usuario = request.user
    if request.method == "POST":
        dados = request.POST.dict()
        nome = dados.get("nome")
        cpf = dados.get("cpf")
        telefone = dados.get("telefone")
        senha = dados.get("senha")
        
        confirma_senha = authenticate(request, username=usuario.username, password=senha)
        
        funcionario, criado = Funcionario.objects.get_or_create(cpf=cpf)
        if not criado:
            return redirect('completar_cadastro')
        elif criado and confirma_senha:
            funcionario.usuario = usuario
            funcionario.nome = nome
            funcionario.telefone = telefone
            criar_usuario_postgre(nome, senha, 'gerente')
            funcionario.save()
            return redirect('home')

    return render(request, 'stock/pages/completar_cadastro.html')

@login_required
def fazer_logout(request):
    logout(request)
    return redirect("fazer_login")

@login_required
@user_passes_test(is_gerente_ou_analista, login_url='/home/')
def exportar_relatorio(request, relatorio):
    if relatorio == "venda":
        informacoes = Venda.objects.filter(finalizada=True)
    elif relatorio == "cliente":
        informacoes = Cliente.objects.all()
    elif relatorio == "funcionario":
        informacoes = Funcionario.objects.all()
    elif relatorio == "itens":
        informacoes = ItensPedido.objects.filter(pedido__finalizada=True)
    return exportar_csv(informacoes)