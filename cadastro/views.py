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
# Create your views hexre. Zz

def index(request):         
    categoria = request.GET.get('categoria', 'Todas categorias')    
    logged = None
    souFornecedor = False
    user = request.user        
    if user != None and user.id != None:#verifica se há alguém logado
        logged = Cliente.cliente.filter(user__id = user.id)                
        if len(logged) == 0:            
            logged = Fornecedor.fornecedor.filter(user__id = user.id)  
            souFornecedor = True

    if categoria != 'Todas categorias':#pega os produtos pela categoria
        produtos_list = Mproduto.produto.filter(categoria=categoria)    
    else:
        produtos_list = Mproduto.produto.all()    
    for produto in produtos_list:
        produto.parcela = '{0:.2f}'.format(produto.valor/produto.divididoAte)    

    paginator = Paginator(produtos_list, 20) # Mostra 20 contatos por página    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        produtos = paginator.page(page)
    except (EmptyPage, InvalidPage):
        produtos = paginator.page(paginator.num_pages)

    inicioPag = 1 #controle da paginação
    now = produtos.number
    fimPag = produtos.paginator.num_pages
    if now >= 4:
        inicioPag = now-4
    if fimPag >= now+10:
       fimPag = now+10
    else:
        fimPag = produtos.paginator.num_pages+1
    user = request.user    
    if logged != None:        
        return render(request,'index.html',{"logged":logged,'souFornecedor':souFornecedor,"produtos":produtos,"range":range(inicioPag,fimPag),'qtd': len(produtos.object_list),'qtdProduto':len(produtos_list),'categoria':categoria,"index":True})                        
    else:
        return render(request,'index.html',{"logged":None,"produtos":produtos,"range":range(inicioPag,fimPag),'qtd': len(produtos.object_list),'qtdProduto':len(produtos_list),'categoria':categoria,"index":True})
def comprar(request):
    logged = None
    user = request.user        
    if user != None and user.id != None:#verifica se há alguém logado
        logged = Cliente.cliente.filter(user__id = user.id)                
        if len(logged) == 0:            
            logged = Fornecedor.fornecedor.filter(user__id = user.id)  
    produto = request.GET.get('produto','')
    produto = Mproduto.produto.get(pk = produto)
    produto.parcela = '{0:.2f}'.format(produto.valor/produto.divididoAte)           
    estoque = produto.estoque

    if request.method == 'POST' and produto.fornecedor.user.id != user.id:#só compra se o o vendedor for diferrente do anunciante
        quantidade = int(request.POST['quantidade'])
        qtdParcelas = int(request.POST.get('qtdParcelas','1'))
        valorTotal = produto.valor*quantidade
        valorDaParcela = '{0:.2f}'.format(valorTotal/qtdParcelas)    
        if produto.estoque > 0:#confima compra, se tiver estoque   
            if logged != None:                
                produto.estoque = produto.estoque-quantidade
                produto.save()
                estoque = produto.estoque
                financeiro = Financeiro.financeiro.create(qtdParcelas = qtdParcelas,valorDaParcela = valorDaParcela)
                financeiro.save()        
                pedido = Pedido.pedido.create(financeiro = financeiro, user = user,produto = produto,quantidade = quantidade,valorTotal = valorTotal).save()                    
                return HttpResponseRedirect('/minha_conta')
            else:
                return render(request,'entrar.html',{})            
    if estoque > 1:
       estoque = range(1,produto.estoque+1)
    divididoAte = produto.divididoAte
    if  produto.divididoAte > 1:
        divididoAte = range(1,produto.divididoAte+1)

    return render(request,'produto.html',{"logged":logged, 'produto': produto,'estoque':estoque,'divididoAte':divididoAte})                        
        
def search(request):
    Post.objects.filter(title__contains='title')
@login_required(login_url='/entrar/')    
def minhaConta(request): 
    fornecedor = False   
    user = request.user  
    deletePedido = request.GET.get('delete','')
    deleteProduto = request.GET.get('produto','')
    pedidos = None   
    if user != None and user.id != None:
        logged = Cliente.cliente.filter(user__id = user.id)                
        if deleteProduto != '':
            try:
                produto = Mproduto.produto.get(pk = deleteProduto)                                     
                produto.delete()
            except Exception, e:
                return HttpResponseRedirect('/minha_conta')
        if deletePedido != '':#exclui o pedido
            try:
                pedido = Mproduto.pedido.get(pk = deletePedido)     
                produto = pedido.produto
                produto.estoque = produto.estoque + pedido.quantidade
                produto.save()
                pedido.delete()
            except Exception, e:
                return HttpResponseRedirect('/minha_conta')
        pedidos = Pedido.pedido.filter(user__id = user.id) 
        if len(logged) == 0:                                
            logged = Fornecedor.fornecedor.filter(user__id = user.id)              
            fornecedor = True
    if fornecedor:
        produtos = Mproduto.produto.filter(fornecedor = logged)
        if len(produtos) == 0:
            produtos = 0
        return render(request,'minha_conta.html',{"logged":logged,'pedidos':pedidos,'qtdpedidos':len(pedidos),'produtos':produtos})
    return render(request,'minha_conta.html',{"logged":logged,'pedidos':pedidos,'produtos':None})

def sair(request):
    logout(request)
    request.session.flush()
    return HttpResponseRedirect('/')

def login_user(request):  
    logout(request)  
    request.session.flush()
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
def novoProduto(request):
    if request.POST:        
        form = ImageProduto(request.POST, request.FILES)                    
        if form.is_valid():                       
            user = request.user        
            logged = Fornecedor.fornecedor.filter(user__id = user.id)[0]   
            foto = form.cleaned_data['image']
            titulo =  request.POST['titulo']
            estoque = request.POST['estoque']
            categoria = request.POST['categoria']
            tipo = request.POST['tipo']            
            divididoAte = float(request.POST['divididoAte'])
            descricao = request.POST['descricao']
            valor = float(request.POST['valor'])            
            parcela = '{0:.2f}'.format(valor/divididoAte)    
            if foto == None:
                produto = Mproduto.produto.create(fornecedor = logged,titulo= titulo,estoque= estoque,categoria = categoria, tipo=tipo,divididoAte = divididoAte,descricao=descricao,valor=valor,parcela=parcela)   
            else:
                produto = Mproduto.produto.create(fornecedor = logged,titulo= titulo,estoque= estoque,categoria = categoria, tipo=tipo,foto =foto,divididoAte = divididoAte,descricao=descricao,valor=valor,parcela=parcela)
            produto.save()
            return HttpResponseRedirect('/minha_conta')
    return render(request,'newproduto.html',{'select':range(1,21)})
@login_required(login_url='/entrar/')    
def continuar(request):            
    user = request.user    
    logged = Cliente.cliente.filter(user__id = user.id)          

    if len(logged) == 0:            
        logged = Fornecedor.fornecedor.filter(user__id = user.id)           
    for x in logged:
        logged = x
  
    if request.method == 'POST':                                                
        endereco = logged.endereco
        endereco.enderecoStr = request.POST['endereco']
        endereco.cep = request.POST['cep']
        endereco.tipo = request.POST['tipo']
        endereco.complemento = request.POST['complemento']
        endereco.estado = request.POST['estado']
        endereco.numero = request.POST['numero']
        endereco.save()

        telefone = logged.telefone
        telefone.numero = request.POST['celular']
        telefone.save()

        documento = logged.documento
        documento.numero = request.POST['cpf']
        documento.save()
        return HttpResponseRedirect('/')                     
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
                return render(request,'cadastrar.html',{})
        else:            
            return render(request,'cadastrar.html',{})
    return render(request,'cadastrar.html',{"cadastrado":''})         
