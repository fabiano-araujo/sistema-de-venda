# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import date
		
class Endereco(models.Model):
    TIPOS = (
        ('Residencial', 'Residencial'),
        ('Trabalho', 'Trabalho'),
        ('Comercial', 'Comercial'),                
    )    
    tipo = models.CharField(max_length=1, choices=TIPOS,default='Residencial')
    numero = models.IntegerField(default=1)
    cep = models.CharField(max_length=250,verbose_name='Cep',default='1')
    complemento = models.CharField(max_length=250,verbose_name='Complemento',default='vazio')    
    estado = models.CharField(max_length=250,verbose_name='Estado',default='vazio')
    enderecoStr = models.CharField(max_length=250,verbose_name='Endereço',default='vazio')
    endereco = models.Manager()	
class Documento(models.Model):
	TIPOS = (
        ('CPF', 'CPF'),
        ('RG', 'RG'),        
    )    
	tipo = models.CharField(max_length=1, choices=TIPOS,default='CPF')
	emicao = models.DateField(("Data de emição"), default=date.today)
	numero = models.CharField(max_length=250,verbose_name='Número',default='vazio')
	documento = models.Manager()	
class Telefone(models.Model):
	TIPOS = (
        ('Residencial', 'Residencial'),
        ('Trabalho', 'Trabalho'),
        ('Comercial', 'Comercial'),        
    )      
	tipo = models.CharField(max_length=1, choices=TIPOS,default='Residencial')
	numero = models.CharField(max_length=250,verbose_name='Número',default='vazio')
	telefone = models.Manager()	

class Cliente(models.Model):
	class Meta:		
		verbose_name = 'Cliente'
		verbose_name_plural = 'Clientes'
	user = models.ForeignKey(User)		
	foto = models.ImageField(upload_to = 'fotos/clientes/', default = 'fotos/user/person-flat.png')
	documento = models.ForeignKey(Documento)
	endereco = models.ForeignKey(Endereco)
	telefone = models.ForeignKey(Telefone)
	cliente = models.Manager()	
class Fornecedor(models.Model):
	class Meta:		
		verbose_name = 'Fornecedor'
		verbose_name_plural = 'Fornecedores'
	user = models.ForeignKey(User)	
	documento = models.ForeignKey(Documento)
	endereco = models.ForeignKey(Endereco)
	telefone = models.ForeignKey(Telefone)
	foto = models.ImageField(upload_to = 'fotos/fornecedores/', default = 'fotos/user/person-flat.png')	
	fornecedor = models.Manager()
class Mproduto(models.Model):
	class Meta:		
		verbose_name = 'Produto'
		verbose_name_plural = 'Produtos'	
	CATEGORIA = (
        ('Animais', 'Animais'),
        ('Comidas', 'Comidas'),        
        ('Eletrodomésticos', 'Eletrodomésticos'),  
        ('Games', 'Games'),  
        ('Livros', 'Livros'),  
        ('Antiguidades', 'Antiguidades'),  
        ('Veículos', 'Veículos'),  
        ('Música', 'Música'),  
        ('Outros', 'Outros'),  
    ) 
	TIPOS = (
        ('novo', 'Novo'),
        ('usado', 'Usado'),      
    )           
        fornecedor = models.ForeignKey(Fornecedor)
	tipo = models.CharField(max_length=20, choices=TIPOS,default='novo')
	categoria = models.CharField(max_length=20, choices=CATEGORIA,default='Outros')	
	foto = models.ImageField(upload_to = 'fotos/produtos/', default = 'fotos/produtos/produto.png')
	titulo = models.CharField(max_length=250,verbose_name='Título')	
	descricao = models.CharField(max_length=300,verbose_name='Descricao')	
	estoque = models.IntegerField(default=1)	
	vendidos = models.IntegerField(default=0)	
	valor = models.DecimalField(max_digits=15, decimal_places=2, default=1)
	unidade  = models.CharField(max_length=300,verbose_name='Unidade')	
	divididoAte = models.IntegerField(default=1)
	parcela = models.DecimalField(max_digits=15, decimal_places=2, default=1)
	produto = models.Manager()	
	def __unicode__(self):
		return self.titulo

class Financeiro(models.Model):	
	qtdParcelas = models.IntegerField(default=1)
	valorDaParcela = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
	Desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
	valorPago = models.DecimalField(max_digits=15, decimal_places=2, default=0)
	financeiro = models.Manager()	
class Pedido(models.Model):		
	produto = models.ForeignKey(Mproduto)
	user = models.ForeignKey(User)
	financeiro = models.ForeignKey(Financeiro)
	quantidade = models.IntegerField(default=1)	
	valorTotal = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
	pedido = models.Manager()	
