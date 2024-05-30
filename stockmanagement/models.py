from django.db import models

# Create your models here.

class Fornecedor(models.Model):
    cnpj = models.BigIntegerField(default=0)
    nome_fornecedor = models.CharField(max_length=45)

    def __str__(self):
        return self.nome_fornecedor


class Produto(models.Model):  
    tb_fornecedores_for_codigo = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    pro_valor = models.FloatField()
    pro_quantidade = models.IntegerField()

    def __str__(self):
        return f"Código: {self.id}, Valor: {self.pro_valor}, Quantidade: {self.pro_quantidade}"


class Funcionario(models.Model): 
    fun_nome = models.CharField(max_length=45)
    fun_cpf = models.CharField(max_length=45)
    fun_senha = models.CharField(max_length=45)
    fun_funcao = models.CharField(max_length=45)

    def __str__(self):
        return self.fun_nome


class Venda(models.Model): 
    ven_horario = models.DateTimeField()  
    ven_valor_total = models.FloatField()
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
