from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Cargo(models.Model):
    cargo = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.cargo

class Funcionario(models.Model):
    cpf = models.CharField(max_length=11, unique=True)  
    nome = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20, blank=True)  
    funcao = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True) 
    usuario = models.OneToOneField(User, max_length=200, null=True, blank=True, on_delete=models.CASCADE, related_name='funcionario')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
    

class Fornecedor(models.Model):
    cnpj = models.CharField(max_length=18, unique=True) 
    nome_fornecedor = models.CharField(max_length=45)

    def __str__(self):
        return self.nome_fornecedor


class Produto(models.Model):  
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tamanho = models.CharField(max_length=10)
    descricao = models.TextField(max_length=100)
    cor = models.TextField(max_length=100)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return f"Descrição: {self.descricao}, Valor: {self.valor}, Quantidade: {self.quantidade}"   


class Cliente(models.Model):
    nome = models.CharField(max_length=60)
    cpf = models.CharField(max_length=11, unique=True) 
    telefone = models.CharField(max_length=20, blank=True) 

    def __str__(self):
        return self.nome

class Venda(models.Model): 
    horario = models.DateTimeField(blank=True, null=True)  
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    funcionario = models.ForeignKey(Funcionario, blank=True, on_delete=models.PROTECT)
    finalizada = models.BooleanField(default=False, blank=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"Código: {self.id}, Horário: {self.horario}, Valor Total: {self.valor_total}"


class ItensPedido(models.Model):
    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)
    pedido =  models.ForeignKey(Venda, null=True, blank=True, on_delete=models.CASCADE)
    preco_parcial = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self) -> str:
        return f"Id: {self.id} - Produto: {self.produto.descricao}, {self.produto.tamanho}, {self.produto.cor}"

