# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import date
	
class Financeiro(models.Model):
	qtdParcelas = models.IntegerField(default=1)
	valorDaParcela = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
	Desconto = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
	valorPago = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
	financeiro = models.Manager()		
class Endereco(models.Model):
    TIPOS = (
        ('R', 'Residencial'),
        ('T', 'Trabalho'),
        ('C', 'Comercial'),        
    )    
    tipo = models.CharField(max_length=1, choices=TIPOS,default='Residencial')
    numero = models.IntegerField(default=1)
    cep = models.CharField(max_length=250,verbose_name='Cep',default='1')
    complemento = models.CharField(max_length=250,verbose_name='Complemento',default='vazio')    
    estado = models.CharField(max_length=250,verbose_name='Estado',default='vazio')
    endereco = models.Manager()	
class Documento(models.Model):
	TIPOS = (
        ('C', 'CPF'),
        ('R', 'RG'),        
    )    
	tipo = models.CharField(max_length=1, choices=TIPOS,default='CPF')
	emicao = models.DateField(("Data de emição"), default=date.today)
	numero = models.CharField(max_length=250,verbose_name='Número',default='vazio')
	documento = models.Manager()	
class Telefone(models.Model):
	TIPOS = (
        ('R', 'Residencial'),
        ('T', 'Trabalho'),
        ('C', 'Comercial'),        
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
class Produto(models.Model):
	class Meta:		
		verbose_name = 'Produto'
		verbose_name_plural = 'Produtos'	
	fornecedor = models.ForeignKey(Fornecedor)
	foto = models.ImageField(upload_to = 'fotos/produtos/', default = 'fotos/user/person-flat.png')
	titulo = models.CharField(max_length=250,verbose_name='Título')	
	descricao = models.CharField(max_length=300,verbose_name='Descricao')	
	estoque = models.IntegerField(default=1)
	valor  = models.IntegerField(default=1)
	unidade  = models.CharField(max_length=300,verbose_name='Unidade')	
	divididoAte = models.IntegerField(default=1)
	produto = models.Manager()	
	def __unicode__(self):
		return self.titulo

class Pedido(models.Model):		
	produto = models.ForeignKey(Produto)
	quantidade = models.IntegerField(default=1)	
	valorTotal = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
	pedido = models.Manager()	
