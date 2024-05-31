from django.db import models

# Create your models here.

class Fornecedor(models.Model):
    cnpj = models.BigIntegerField(default=0)
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
    

class Funcionario(models.Model): 
    fun_nome = models.CharField(max_length=60)
    fun_cpf = models.BigIntegerField()
    fun_senha = models.CharField(max_length=45)
    fun_funcao = models.CharField(max_length=45)

    def __str__(self):
        return self.fun_nome


class Cliente(models.Model):
    cli_nome = models.CharField(max_length=60)
    cli_cpf = models.BigIntegerField()
    cli_telefone = models.BigIntegerField()


class Venda(models.Model): 
    ven_horario = models.DateTimeField()  
    ven_valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    tb_funcionarios_fun_codigo = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Código: {self.id}, Horário: {self.ven_horario}, Valor Total: {self.ven_valor_total}"


class Item(models.Model):
    tb_produtos_pro_codigo = models.ForeignKey(Produto, on_delete=models.CASCADE)
    ite_quantidade = models.IntegerField()
    ite_valor_parcial = models.FloatField()
    tb_vendas_ven_codigo = models.ForeignKey(Venda, on_delete=models.CASCADE)

    def __str__(self):
        return f"Código: {self.id}, Quantidade: {self.ite_quantidade}, Valor Parcela: {self.ite_valor_parcela}"
