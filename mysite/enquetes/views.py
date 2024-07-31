from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Pergunta, Escolha
from django.db.models import F
from django.urls import reverse

def index(request):
    ultimas_perguntas = Pergunta.objects.order_by("-data_publicacao")[:5]
    contexto = { 'ultimas_perguntas': ultimas_perguntas}
    return render(request,'enquetes/index.html',contexto)

def detalhes(request, pergunta_id):
    try:
        pergunta = Pergunta.objects.get(pk=pergunta_id)
    except:
        raise Http404("A pergunta não existe!")
    return render(request, 'enquetes/detalhes.html',{'pergunta':pergunta})

def resultados(request, pergunta_id):
   pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
   return render(request, "enquetes/resultado.html",{"pergunta": pergunta})

def votos(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    try:
        escolha_selecionada = pergunta.escolha_set.get(pk=request.POST["escolha"])
    except (KeyError, Escolha.doesNotExist):
        return render(
            request,
            "enquetes/detalhes.html",
            {
                "question": pergunta,
                "error_message": "você não selecionou uma escolha.",

            },
        )
    else:
        escolha_selecionada.voto = F("votos") + 1
        escolha_selecionada.save()
        return HttpResponseRedirect(reverse("enquetes:resultado", args=(pergunta.id,)))