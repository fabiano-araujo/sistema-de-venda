# -*- encoding: utf-8 -*-
"""venda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$','cadastro.views.index',name = 'index'),        
    url(r'^entrar/','cadastro.views.login_user',name = 'entrar'),    
    url(r'^cadastrar/','cadastro.views.cadastrar',name = 'cadastrar'),    
    url(r'^continue/','cadastro.views.continuar',name = 'continue'),    
    url(r'^novo_produto/','cadastro.views.novoProduto',name = 'novoProduto'),    
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': './media/'}),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': './static/',}),    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^sair/','cadastro.views.sair',name = 'sair'),  
    url(r'^comprar/','cadastro.views.comprar',name = 'comprar'),  
    url(r'^minha_conta/','cadastro.views.minhaConta',name = 'minhaConta'),       
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)