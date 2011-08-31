# Create your views here.
#coding:utf-8


from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context, Template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.localflavor.br.forms import BRPhoneNumberField
from django.core.paginator import Paginator
from alunoVoluntario.cadastro.models import Estudante,Certificado
from django.core.mail import send_mail, get_connection, EmailMessage
from django.contrib.auth.decorators import login_required
from datetime import date
from django.forms import HiddenInput
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from cStringIO import StringIO
from datetime import datetime
import datetime
import os

def adicionar(request):
    f = EstudanteModelForm()
    if request.POST:
        f = EstudanteModelForm(request.POST)
        if f.is_valid():
            email = request.POST.get('Email')
            estudante = f.save()
	    send_mail('Recebemos sua inscrição', 
                      'Sua inscrição para aluno voluntário foi cadastrada com sucesso, aguarde confirmação da sua participação.',
                      '',#email do remetente
                      [email],
                      fail_silently=False) 
            return HttpResponseRedirect('/')
    return render_to_response('adicionar.html', {'form':f}, context_instance=RequestContext(request))

           
@login_required
def enviar_email(request, codigo):
    estudante = get_object_or_404(Estudante, pk=codigo)
    email = estudante.Email
    estudante.email_env = 'Sim'
    estudante.save()
    send_mail('Confirmação para Renunião do Aluno Voluntário', 
              'Você foi convocado para a reunião.',
              '',#email do remetente
              [email],
              fail_silently=False)
    return HttpResponseRedirect('/relatorio-inscritos/')


@login_required
def listar(request, codigo):
    estudante = get_object_or_404(Estudante, pk=codigo)
    codigo = estudante.Codigo
    f = EstudanteForm(instance=estudante)
    if request.method == 'POST':
        f = EstudanteForm(request.POST, instance=estudante)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect('/relatorio')
        else:
            return render_to_response(f.errors)    
    return render_to_response('estudante.html', {'form':f, 'codigo':codigo , 'f':estudante}, context_instance=RequestContext(request))

@login_required
def relatorio_todos(request):
    estudante = Estudante.objects.all()
    return render_to_response('relatorio_todos.html', locals(), context_instance=RequestContext(request))

@login_required
def relatorio(request):
    estudante = Estudante.objects.all()
    return render_to_response('relatorio.html', locals(), context_instance=RequestContext(request))

@login_required
def relatorio_atividade(request, codigo):
    estudante = Estudante.objects.filter(Atividade=codigo)
    if codigo == '1':
        atv = 'Recepção aos Visitantes'
    elif codigo == '2':
        atv = 'Recepção aos Alunos Agendados para Visitas Guiadas'
    elif codigo == '3':
    	atv = 'Auxilio a Biblioteca'
    elif codigo == '4':
	    atv = 'Apoio a Atividades Academicas'
    elif codigo == '5':
	    atv = 'Apoio a Organizacao em Geral'
    elif codigo == '6':
	    atv = 'Apoio a Feitec'
    elif codigo == '7':
	    atv = 'Apoio a Mostre-se'
    elif codigo == '8':
	    atv = 'Apoio a Coordenação de Cultura'
    elif codigo == '9':
	    atv = 'Apoio a Curadoria Educativa'
    return render_to_response('relatorio_atividade.html', {'atv':atv, 'estudante':estudante}, context_instance=RequestContext(request))

@login_required
def principal_certificado(request):
     return render_to_response('certificado.html', context_instance = RequestContext(request))

#Exibir todos participantes
@login_required
def todos_voluntarios(request):
     part = Estudante.objects.all()
     return render_to_response('todos_voluntarios.html',locals(), context_instance=RequestContext(request))

@login_required
def editar_participante(request, codigo):
    estudante = get_object_or_404(Estudante, pk=codigo)
    if request.method == 'POST':
        form = SituacaoIntModelForm(request.POST, instance=estudante)
        if form.is_valid():
            c = form.save()
            return HttpResponseRedirect(reverse('alunoVoluntario.views.relatorio_atividade'))
        else:
            return render_to_response(form.errors)
    else:
        form = SituacaoIntModelForm(instance=estudante)
        participante = Estudante.objects.get(Codigo = codigo)
        return render_to_response('editar_participante.html',{'form':form, 'participante':participante, 'codigo':codigo,}, context_instance=RequestContext(request))

#Busca de participante
@login_required
def busca_voluntarios(request):
    if request.method =='POST':
        nome = request.POST['nome']
        part = Estudante.objects.filter(Nome__icontains=nome)
        return render_to_response('busca_vol.html',{'part':part,}, context_instance=RequestContext(request))
    else:
        return render_to_response('busca_vol.html', context_instance=RequestContext(request))

#emitir certificado do participante
@login_required
def emitir(request, codigo):
    usuario = request.user
    x = get_object_or_404(Estudante, pk=codigo)
    try:
        certificado = Certificado.objects.get(estudante = codigo)
    except ObjectDoesNotExist:
        certificado = Certificado.objects.create(estudante = x)
    if request.method =='POST':    
        f= DadosCertModelForm(request.POST,instance = certificado)
        if f.is_valid():        
            c = f.save()
            return HttpResponseRedirect(reverse('alunoVoluntario.cadastro.views.certificado', args=[x.Codigo, c.codCert]))
        else:
            render_to_response(f.errors)
    else:
        f= DadosCertModelForm(instance = certificado)
        return render_to_response('dadoscertificado.html', {'c':x, 'f':f,'usuario':usuario,}, context_instance=RequestContext(request))

#gerar pdf do certificado do participante
@login_required
def certificado(request,codigo, codCert): 
        response = HttpResponse (mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=certificado.pdf'
        buffer = StringIO()
        p = canvas.Canvas(buffer)
        
        d = get_object_or_404(Certificado, pk=codCert)
        c = get_object_or_404(Estudante, pk=codigo)
        dia = str (d.data)
        mes = str (d.mes)
        ano = str (d.ano)
        

        p.translate(inch,inch)
        p.setFont("Helvetica", 14)
        p.rotate(90)
        #image = os.path.join("Certificado.png")
        artur = os.path.join("carlos.png") 
        jeff = os.path.join("jeff.png") 
        p.drawImage(artur, 1*inch,-400, width=91,height=50)
        p.drawImage(jeff, 7*inch,-400, width=180,height=50) 
        #p.drawImage(image, -1.0*inch,-550, width=840,height=620)
        p.setFont("Helvetica-BoldOblique", 12)
        p.drawString(1*inch, -220, "Certificamos que " + c.Nome + " participou da Semana do Saber como aluno voluntário.")
        p.drawString(6*inch, -260, "Campos dos Goytacazes, " + dia + " de " + mes + " de " + ano)
        p.setFont("Helvetica-BoldOblique", 12)
        p.drawString(0.7*inch, -415, "Carlos Artur de Carvalho Arêas")  
        p.setFont("Helvetica-Oblique", 12)
        p.drawString(0.5*inch, -430, "Diretor do Departamento de Desenvolvimento") 
        p.drawString(0.3*inch, -445, "Institucional e Extensão Campus Campos-Centro")
        p.setFont("Helvetica-BoldOblique", 12)
        p.drawString(7*inch, -415, "Jefferson Manhães de Azevedo") 
        p.setFont("Helvetica-Oblique", 12) 
        p.drawString(7.5*inch, -430, "Diretor Geral do IFF") 
        p.drawString(7.3*inch, -445, "Campus Campos-Centro")       
        p.setFont("Helvetica", 8)
        p.drawString(8*inch,-490, "O presente certificado foi registrado sob o n." + d.numeroCert)        
        p.drawString(8*inch, -500, "No Livro n. " + d.livroCert + " em " + d.dataCert)
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

class DadosCertModelForm(forms.ModelForm):
    class Meta:
        model = Certificado
        widgets = {
            'estudante':HiddenInput(),
        }

class EstudanteModelForm(forms.ModelForm):
    celular = BRPhoneNumberField(label="Celular")
    class Meta:
        exclude = ('email_env', 'participacao')
        model = Estudante

class EstudanteForm(forms.ModelForm):
    class Meta:
        model = Estudante
        widgets = { 
                'Nome' : HiddenInput(),
                'Codigo': HiddenInput(),
                'Matricula' : HiddenInput(),
                'celular' : HiddenInput(),
                'Email' : HiddenInput(),
                'Campus' : HiddenInput(),
                'Disponibilidade' : HiddenInput(),
                'Horario' : HiddenInput(),
                'Horario_Fim' : HiddenInput(),
                'Tamanho' : HiddenInput(),
                'Data' : HiddenInput(),
                'email_env' : HiddenInput(),
        }



