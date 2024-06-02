from .models import *
import psycopg2
from psycopg2 import sql
from django.conf import settings



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
        print("foi")
        cur.execute(sql.SQL("GRANT {} TO {}").format(sql.Identifier(cargo), sql.Identifier(nome)))
        print("foi")


        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")

