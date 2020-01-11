from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryFrom


# Create your views here.
def index(request):
    """A página inicial de learning Log"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Mostra todos os assuntos."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Mostra um único assunto e todas as suas entradas."""
    topic = get_object_or_404(Topic, id=topic_id)
    # Garante que o assunto pertence ao usuario atual
    check_topic_owner(request, topic)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Adiciona um novoassunto."""
    #  Nenhum dado submetido; cria um formulario em branco
    if request.method != 'POST':
        # Nenhum dado submetido; cria um formulário em branco
        form = TopicForm()
    else:
        # Dados de POST submetidos; processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse_lazy('learning_logs:topics'))
    context = {'form': form}
    return render(
        request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Adiciona uma nova entrada para um assunto em particular."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # Nenhum dado submetido; cira um formulario em branco
        form = EntryFrom()
    else:
        # Dados de POST submetidos; processa os dados
        form = EntryFrom(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return HttpResponseRedirect(
                reverse_lazy('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edita uma entrada existente."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # Reqquisição inicial; preenche previamente o formulário com a entrada
        # atual
        form = EntryFrom(instance=entry)
    else:
        # Dados de POST submetidos; processa os dados
        form = EntryFrom(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse_lazy('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


# Checa se os topicos pertence a um usuario.
@login_required
def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404
