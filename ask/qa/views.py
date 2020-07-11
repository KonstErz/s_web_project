from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Question, Answer
from django.views.decorators.http import require_GET


def test(request, *args, **kwargs):
    return HttpResponse('OK')

"""
def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return paginator, page
"""


def question_list(request):
    qs = Question.objects.new()
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, limit)
    paginator.baseurl = '/?page='
    page = paginator.page(page)
    return render(request, 'qa/question_list_new.html',
                  context={'questions': page.object_list,
                           'paginator': paginator,
                           'page': page},
                  )


def popular(request):
    qs = Question.objects.popular()
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, limit)
    paginator.baseurl = '/popular/?page='
    page = paginator.page(page)
    return render(request, 'qa/question_list_popular.html',
                  context={'questions': page.object_list,
                           'paginator': paginator,
                           'page': page},
                  )


@require_GET
def question_details(request, id):
    question = get_object_or_404(Question, id=id)
    try:
        answers = Answer.objects.filter(question=question)
    except Answer.DoesNotExist:
        answers = None
    return render(request, 'qa/question_detail.html',
                  context={'question': question,
                           'answers': answers},
                  )
