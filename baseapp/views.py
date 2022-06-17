import email
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator

from .models import *
from .forms import *


class ProjectDetailView(DetailView):
    model = Projects


def Home(request):
    busca = request.GET.get('busca')
    if busca:
        project_list = Projects.objects.filter(title__icontains=busca)

    else:
        project_list = Projects.objects.all()
        paginator = Paginator(project_list, 4)

        page = request.GET.get('page')
        project_list = paginator.get_page(page)

    if request.method == 'POST':
        form = ContatoForm(request.POST)
        form.save()
        if form.is_valid():
            messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('/')
    else:
        form = ContatoForm()

    return render(request, 'baseapp/index.html', {'project_list': project_list, 'form': form})


def Email(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        form.save()
        if form.is_valid():
            messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('/')
    else:
        form = ContatoForm()
        return render(request, 'baseapp/index.html', {'form': form})
