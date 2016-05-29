# -*- encoding: utf-8 -*-
from django.contrib import admin
from cadastro.models import *
	
class ClienteAdmin(admin.ModelAdmin):	
	search_fields = ['foto']
	list_display = ['foto','user']	
	list_filter = ['foto']
	save_on_top = True	

class FornecedorAdmin(admin.ModelAdmin):	
	search_fields = ['foto']
	list_display = ['foto','user','documento','telefone','endereco']	
	list_filter = ['foto']
	save_on_top = True	

admin.site.register(Cliente,ClienteAdmin)	
admin.site.register(Mproduto)
admin.site.register(Pedido)
admin.site.register(Endereco)
admin.site.register(Financeiro)
admin.site.register(Documento)
admin.site.register(Telefone)
admin.site.register(Fornecedor,FornecedorAdmin)	