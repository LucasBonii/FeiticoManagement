from .models import *

def calcular_preco_parcial(item_pedido):
    total = 0
    return float(item_pedido.produto.valor * item_pedido.quantidade)


def calcular_preco_total(venda):
    total = 0
    itens_venda = ItensPedido.objects.filter(pedido=venda)
    total = sum([item.preco_parcial for item in itens_venda])
    return total


def verificar_quantidades(venda):
    itens_pedido = ItensPedido.objects.filter(pedido=venda)
    if len(itens_pedido) < 1:
        return False
    for item in itens_pedido:
        if item.quantidade > item.produto.quantidade:
            return False
    return True