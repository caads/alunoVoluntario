#coding:utf-8
from django.db import models
from datetime import date
# Create your models here.

horarios = (
    (u'14', u'14:00'),
    (u'15', u'15:00'),
    (u'16', u'16:00'),
    (u'17', u'17:00'),
    (u'18', u'18:00'),
    (u'19', u'19:00'),
    (u'20', u'20:00'),
    (u'21', u'21:00'),
    (u'22', u'22:00'),
)

datas = (
    (u'7', u'07/09'),
    (u'8', u'08/09'),
    (u'9', u'09/09'),
    (u'Todos', u'Todos os Dias'),
)
CAMPUS_CHOICES = (
    ('Campos-Centro', 'Campus-Centro'),
    ('Guarus', 'Guarus'),
    ('Macae', 'Macae'),
	('Quissama', 'Quissama'),
    ('Itaperuna', 'Itaperuna'),
    ('Cabo-Frio', 'Cabo-Frio'),
)

participou = (
    ('S', 'Sim'),
    ('N', 'Não'),
)

ATIVIDADES_CHOICES = (
    ('1', 'Recepção aos Visitantes'),
    ('2', 'Recepção aos Alunos Agendados para Visitas Guiadas'),
	('3', 'Auxilio a Biblioteca'),
    ('4', 'Apoio a Atividades Academicas'),
  	('5', 'Apoio a Organizacao em Geral'),
    ('6', 'Apoio a Feitec'),
    ('7', 'Apoio a Mostre-se'),
    ('8', 'Apoio a Coordenação de Cultura'),
    ('9', 'Apoio a Curadoria Educativa'),
)

DISPONIBILIDADE_CHOICES = (
    ('Tarde', 'Tarde'),
    ('Noite', 'Noite'),
)

TAMANHOCAMISA_CHOICES = (
    ('P', 'P'),
    ('M', 'M'),
	('G', 'G'),
    ('GG', 'GG'),
  	('XG', 'XG'),
)

EMAIL_CHOICES = (
    ('Sim', 'Sim'),
    ('Nao', 'Nao'),
)

class Choices(models.Model):    
    datas = (
        (u'7', u'07/09'),
        (u'8', u'08/09'),
        (u'9', u'09/09'),
    )
    dia = (
        (u'01', u'01'),
        (u'02', u'02'),
        (u'03', u'03'),
        (u'04', u'04'),
        (u'05', u'05'),
        (u'06', u'06'),
        (u'07', u'07'),
        (u'08', u'08'),
        (u'09', u'09'),
        (u'10', u'10'),
        (u'11', u'11'),
        (u'12', u'12'),
        (u'13', u'13'),
        (u'14', u'14'),
        (u'15', u'15'),
        (u'16', u'16'),
        (u'17', u'17'),
        (u'18', u'18'),
        (u'19', u'19'),
        (u'20', u'20'),
        (u'21', u'21'),
        (u'22', u'22'),
        (u'23', u'23'),
        (u'24', u'24'),
        (u'25', u'25'),
        (u'26', u'26'),
        (u'27', u'27'),
        (u'28', u'28'),
        (u'29', u'29'),
        (u'30', u'30'),
        (u'31', u'31'),       
    )

    mes = (
        (u'Janeiro', u'Janeiro'),
        (u'Fevereiro', u'Fevereio'),
        (u'Março', u'Março'),
        (u'Abril', u'Abril'),
        (u'Maio', u'Maio'),
        (u'Junho', u'Junho'),
        (u'Julho', u'Julho'),
        (u'Agosto', u'Agosto'),
        (u'Setembro', u'Setembro'),
        (u'Outubro', u'Outubro'),
        (u'Novembro', u'Novembro'),
        (u'Dezembro', u'Dezembro'),
   )
   
    ano = (
        (u'2011', u'2011'),
        (u'2012', u'2012'),
        (u'2013', u'2013'),
    )


class Estudante(models.Model):
    class Meta:
        ordering = ('-Nome',)

    Codigo = models.AutoField('Codigo', primary_key=True, db_index=True)
    Matricula = models.CharField('Matricula', db_index=True, max_length=12,unique=True)
    Nome = models.CharField('Nome', db_index=True, max_length=100)
    celular = models.CharField('Celular', max_length=14)
    Email = models.EmailField('E-mail', max_length=100)    
    Campus = models.CharField('Campus', max_length=100, choices=CAMPUS_CHOICES)
    Atividade = models.CharField('Atividade', max_length=100, choices=ATIVIDADES_CHOICES)
    Disponibilidade = models.CharField('Disponibilidade', max_length=100, choices=DISPONIBILIDADE_CHOICES)
    Horario = models.CharField('Horario Inicial', max_length=100, choices=horarios)
    Horario_Fim = models.CharField('Horario Final', max_length=100, choices=horarios)
    Tamanho = models.CharField('Tamanho da Camisa', max_length=2, choices=TAMANHOCAMISA_CHOICES)
    Data = models.CharField('Data', max_length=14, choices=datas)
    participacao = models.CharField('Participou?', max_length=1, choices=participou, default= 'N')
    email_env = models.CharField('Email Enviado', max_length=3, choices=EMAIL_CHOICES, default='Nao')
    class Admin:
        pass

    def __unicode__(self):
        return self.Nome
    
    def get_absolute_url(self):
        return '/estudante/%d/'%(self.Codigo)

class Certificado(models.Model):
    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'

    codCert = models.AutoField(primary_key=True)
    numeroCert= models.CharField("Numero",max_length=10,default = "00",blank=True)
    livroCert= models.CharField("Livro", max_length=10,default = "00",blank=True)
    dataCert= models.CharField("Data", max_length=10,default = "--/--/----",blank=True)
    data = models.CharField("Data", max_length=10, choices = Choices.dia, blank = True)
    mes = models.CharField("Mes", max_length=20, choices = Choices.mes, blank = True)
    ano = models.CharField("Ano", max_length=10, choices = Choices.ano, blank = True)
    estudante = models.ForeignKey('Estudante')
