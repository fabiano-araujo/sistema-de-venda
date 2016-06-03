# -*- coding:utf-8 -*-
from django import forms
from django.forms import CharField, Form, PasswordInput,ModelForm
from django.contrib.admin import widgets         
from django.contrib.auth.models import User
from cadastro.models import *
from django.contrib.admin.widgets import AdminFileWidget


class FormLogin(forms.Form):
	usuario=forms.CharField(label='Usuário',required=True)
	senha=forms.CharField(label='Senha', required=True)

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField(required=False)
    username = forms.CharField(label='username',required=True)
    email = forms.EmailField(required=False)
    password = forms.CharField(label='password',required=True)
    confimarPassword = forms.CharField(label='confimarPassword',required=False)
    souFuncionario = forms.BooleanField(required=False)
class ImageProduto(forms.Form): 
	image = forms.ImageField(required=False)
class MyUser ():
    def getUser(request,str):
        logged = None
        user = request.user        
        if user != None and user.id != None:#verifica se há alguém logado
            logged = Cliente.cliente.filter(user__id = user.id)                
            if len(logged) == 0:            
                logged = Fornecedor.fornecedor.filter(user__id = user.id)  
        return logged