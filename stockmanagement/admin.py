from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Funcionario)
admin.site.register(Venda)
admin.site.register(Produto)
admin.site.register(ItensPedido)
admin.site.register(Fornecedor)
admin.site.register(Cargo)