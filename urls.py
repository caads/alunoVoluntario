from django.conf.urls.defaults import *
from alunoVoluntario.cadastro.views import *
from django.conf import settings
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from cadastro.models import Estudante
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'alunoVoluntario.cadastro.views.adicionar', name='home'),
    # url(r'^meucad/', include('meucad.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^estudante/(?P<codigo>\d+)/$', 'alunoVoluntario.cadastro.views.listar'),
    url(r'^relatorio/$', 'alunoVoluntario.cadastro.views.relatorio'),
    url(r'^relatorio-inscritos/$', 'alunoVoluntario.cadastro.views.relatorio_todos'),
    url(r'^relatorio-atividade/(?P<codigo>\d+)/$', 'alunoVoluntario.cadastro.views.relatorio_atividade'),
    url(r'^enviar-email/(?P<codigo>\d+)/$', 'alunoVoluntario.cadastro.views.enviar_email'),
    url(r'^principal_certificado/$', 'alunoVoluntario.cadastro.views.principal_certificado'),
    url(r'^todos_voluntarios/$', 'alunoVoluntario.cadastro.views.todos_voluntarios'),
    url(r'^busca_voluntarios/$', 'alunoVoluntario.cadastro.views.busca_voluntarios'),
    url(r'^emitir/(?P<codigo>\d+)/$','alunoVoluntario.cadastro.views.emitir'),
    url(r'^certificado/(?P<codigo>\d+)/(?P<codCert>\d+)/$','alunoVoluntario.cadastro.views.certificado'),
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'logout.html', 'next_page': '/login'}),

)
