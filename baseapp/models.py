from contextlib import nullcontext
from distutils.command.upload import upload
from pyexpat import model
from random import choices
import smtplib
from venv import create
from django.db import models
from django.forms import SlugField
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from smtplib import SMTPAuthenticationError
from django.core.mail import send_mail
from django.conf import settings
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Projects(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextField()
    body = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to='posts', null=True, blank=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project:detail", kwargs={"slug": self.slug})


class Contato(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=120, null=True)
    data = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField(null=True)
    telefone = models.CharField(max_length=20, null=True)
    assunto = models.CharField(max_length=100, null=True)
    mensagem = models.TextField(null=True)
    email_sent = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.nome

    def send_mail(self):
        message_admin = """
		Nova Mensagem - Portifolio Leandro Gonçalves
		Nome: {0}
		Email: {1}
		Telefone: {2}
		Assunto: {3}
		Mensagem: {4}
		"""
        message_admin = message_admin.format(
            self.nome, self.email, self.telefone, self.assunto, self.mensagem)

        message = """
Olá {0},
Obrigado por entrar em contato comigo.
Entrarei em contato o mais breve possivel!
		"""
        message = message.format(self.nome,)

        try:
            send_mail(
                'Novo Contato | Leandro Gonçalves',
                message_admin,
                'Leandro Gonçalves <leandrogoncalves3141@gmail.com>',
                settings.ADMINS,
                fail_silently=False,
            )
            send_mail(
                'Auto Mensagem - Leandro Gonçalves',
                message,
                'Leandro Gonçalves <leandrogoncalves3141@gmail.com>>',
                [self.email],
                fail_silently=False,
            )
            self.email_sent = True
            self.save()
        except smtplib.SMTPAuthenticationError:
            pass


def send_confirmation_email(sender, instance, created, **wkargs):
    if not instance.email_sent:
        instance.send_mail()


models.signals.post_save.connect(
    send_confirmation_email, sender=Contato, dispatch_uid='contato.Record')
