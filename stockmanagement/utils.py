from stockmanagement .models import *
import psycopg2
from psycopg2 import sql
from django.conf import settings
import csv
from django.http import HttpResponse
from django.shortcuts import redirect




def calcular_preco_parcial(item_pedido):
    total = 0
    return float(item_pedido.produto.valor * item_pedido.quantidade)


def calcular_preco_total(venda):
    total = 0
    itens_venda = ItensPedido.objects.filter(pedido=venda)
    total = sum([item.preco_parcial for item in itens_venda])
    print(total)
    return total


def verificar_quantidades(venda):
    itens_pedido = ItensPedido.objects.filter(pedido=venda)
    if len(itens_pedido) < 1:
        return False
    for item in itens_pedido:
        if item.quantidade > item.produto.quantidade:
            return False
    return True

def diminuir_estoque(venda):
    itens_pedido = ItensPedido.objects.filter(pedido=venda)
    verificar_quantidades(venda)
    for item in itens_pedido:
        item.produto.quantidade -= item.quantidade
        item.save()
        item.produto.save()


def variaveis_conexao():
    db_name = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']

    return db_name, db_user, db_password, db_host, db_port


def criar_usuario_postgre(nome, senha, cargo):
    db_name, db_user, db_password, db_host, db_port = variaveis_conexao()

    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        conn.autocommit = True
        cur = conn.cursor()
        cargo = cargo.lower()
        nome = nome.replace(" ", "")
        nome = nome.lower()
        cur.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(nome)), [senha])
        
        cur.execute(sql.SQL("GRANT {} TO {}").format(sql.Identifier(cargo), sql.Identifier(nome)))
        


        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")


def exportar_csv(informacoes):
    colunas = informacoes.model._meta.fields
    nome_colunas = [coluna.name for coluna in colunas]
    
    resposta = HttpResponse(content_type="text/csv")
    resposta["Content-Disposition"] = f"attachment; filename={informacoes.model._meta.db_table}.csv"

    creator = csv.writer(resposta, delimiter=";")
    creator.writerow(nome_colunas)
    for linha in informacoes.values_list():
        creator.writerow(linha)

    return resposta


def fazer_login_postgre(request, username, password):
    try:
        # Tenta conectar ao PostgreSQL com as credenciais fornecidas
        conn = psycopg2.connect(
            dbname='feiticomanagement',
            user=username,
            password=password,
            host='dpg-cpf0n5dds78s739477dg-a.oregon-postgres.render.com',
            port='5432'
        )
        conn.close()  # Se a conexão for bem-sucedida, as credenciais estão corretas
        
        # Criar uma sessão para o usuário
        request.session['postgres_user'] = username
        return redirect('home')
    except:
        return redirect('fazer_login')



def require_access_level(level):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            try:
                usuario = Funcionario.objects.get(usuario=request.session['postgres_user'])

                if str(usuario.funcao) in level:
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('home')
            except:
                return redirect('completar_cadastro')
             
        return _wrapped_view
    return decorator



def verificar_cadastro(request):
    try:
        username = request.session['postgres_user']
    except:
        return redirect('fazer_login')
    usuario = Funcionario.objects.get(usuario=request.session['postgres_user'])
    if not usuario:
        return redirect('completar_cadastro')

    
