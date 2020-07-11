from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Question, Answer


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def question_list(request):
    qs = Question.objects.all().order_by('-id')
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, limit)
    page = paginator.page(page)
    return render(request, 'question_list.html',
                  {'title': 'New',
                   'questions': page.object_list,
                   'paginator': paginator,
                   'page': page, })


def popular(request):
    qs = Question.objects.all().order_by('-rating')
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, limit)
    page = paginator.page(page)
    return render(request, 'question_list.html',
                  {'title': 'Popular',
                   'questions': page.object_list,
                   'paginator': paginator,
                   'page': page, })


def question_details(request, num):
    try:
        question = Question.objects.get(id=num)
    except Question.DoesNotExist:
        raise Http404
    try:
        answers = Answer.objects.filter(question=question)
    except Answer.DoesNotExist:
        answers = None
    return render(request, 'question_detail.html',
                  {'question': question,
                   'answers': answers, })
