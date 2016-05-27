# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from cadastro.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from cadastro.models import *
from cadastro.forms import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
# Create your views here. Zz

def index(request):         
    categoria = request.GET.get('categoria', 'Todas categorias')
    if categoria != 'Todas categorias':
        produtos_list = Produto.produto.filter(categoria=categoria)    
    else:
        produtos_list = Produto.produto.all()
    paginator = Paginator(produtos_list, 20) # Mostra 25 contatos por página    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        produtos = paginator.page(page)
    except (EmptyPage, InvalidPage):
        produtos = paginator.page(paginator.num_pages)

    for produto in produtos:
        produto.parcela = produto.valor/produto.divididoAte
    inicioPag = 1
    now = produtos.number
    fimPag = produtos.paginator.num_pages
    if now >= 4:
        inicioPag = now-4
    if fimPag >= now+10:
       fimPag = now+10
    else:
        fimPag = produtos.paginator.num_pages+1
    user = request.user    
    if user != None and user.id != None:
        logged = Cliente.cliente.filter(user__id = user.id)                
        if len(logged) == 0:            
            logged = Fornecedor.fornecedor.filter(user__id = user.id)  
        return render(request,'index.html',{"logged":logged,"produtos":produtos,"range":range(inicioPag,fimPag),'qtd': len(produtos.object_list),'qtdProduto':len(produtos_list),'categoria':categoria})                        
    else:
        return render(request,'index.html',{"logged":None,"produtos":produtos,"range":range(inicioPag,fimPag),'qtd': len(produtos.object_list),'qtdProduto':len(produtos_list),'categoria':categoria})
@login_required(login_url='/entrar/')    
def minhaConta(request):
    user = request.user    
    if user != None and user.id != None:
        logged = Cliente.cliente.filter(user__id = user.id)                
        if len(logged) > 0:
            return render(request,'minha_conta.html',{"logged":logged})            
        else:
            logged = Fornecedor.fornecedor.filter(user__id = user.id)  
            return render(request,'minha_conta.html',{"logged":logged})                    

def sair(request):
    logout(request)
    request.session.flush()
    return HttpResponseRedirect('/')

def login_user(request):    
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            return render(request,'entrar.html',{})            
    return render_to_response('entrar.html', context_instance=RequestContext(request))

@login_required(login_url='/entrar/')    
def continuar(request):            
    user = request.user    
    logged = Cliente.cliente.filter(user__id = user.id)          

    if len(logged) == 0:            
        logged = Fornecedor.fornecedor.filter(user__id = user.id)           
    for x in logged:
        logged = x
  
    if request.method == 'POST':        
        cep = request.POST['cep']
        numero = request.POST['numero']
        celular = request.POST['celular']
        estado = request.POST['estado']        
        tipo= request.POST['tipo']
        enderecoStr = request.POST['endereco']
        complemento= request.POST['complemento']
        cpf = request.POST['cpf']

        endereco = logged.endereco
        endereco.cep = cep
        endereco.tipo = tipo
        endereco.complemento = complemento
        endereco.estado = estado
        endereco.numero = numero
        endereco.save()

        telefone = logged.telefone
        telefone.numero = celular
        telefone.save()

        documento = logged.documento
        documento.numero = cep
        documento.save()
        
    return render(request,'continue.html',{})                           
def cadastrar(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)                    
        if form.is_valid():            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            foto = form.cleaned_data['image']
            fornecedor = form.cleaned_data['souFuncionario']

            user = User.objects.filter(username = username)
            if len(user) == 0:
                documento = Documento.documento.create()
                endereco = Endereco.endereco.create()
                telefone = Telefone.telefone.create()
                
                user = User.objects.create_user(username, email, password)
                user.save()            
                if fornecedor:
                    if foto != None:
                        f = Fornecedor.fornecedor.create(foto = foto,user = user,documento=documento,telefone = telefone,endereco = endereco)
                        f.save()    
                    else:          
                        f = Fornecedor.fornecedor.create(user = user,documento=documento,telefone = telefone,endereco = endereco)
                        f.save()           
                else:
                    if foto != None:
                        c = Cliente.cliente.create(foto = foto,user = user,documento=documento,telefone = telefone,endereco = endereco)                                
                        c.save()
                    else:          
                        c = Cliente.cliente.create(user = user,documento=documento,telefone = telefone,endereco = endereco)                                
                        c.save()                               
                user = authenticate(username=username, password=password)            
                login(request, user)
                return HttpResponseRedirect('/continue')
            else:
                return render(request,'cadastrar.html',{"cadastrado":form.cleaned_data['image']})
        else:            
            return render(request,'cadastrar.html',{"cadastrado":form.cleaned_data['image']})
    return render(request,'cadastrar.html',{"cadastrado":''})         
