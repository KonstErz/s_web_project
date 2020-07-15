from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from .models import Question, Answer
from .forms import AskForm, AnswerForm
from django.contrib.auth.models import User


def test(request, *args, **kwargs):
    return HttpResponse('OK')


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
    return paginator, page, limit


@require_GET
def question_list(request, *args, **kwargs):
    questions = Question.objects.order_by('-id')
    paginator, page, limit = paginate(request, questions)
    context = {
        'title': 'List of New Questions',
        'questions': page,
        'paginator': paginator,
        'limit': limit,
    }
    return render(request, 'question_list.html', context)


@require_GET
def popular(request, *args, **kwargs):
    questions = Question.objects.popular()
    paginator, page, limit = paginate(request, questions)
    context = {
        'title': 'List of Popular Questions',
        'questions': page,
        'paginator': paginator,
        'limit': limit,
    }
    return render(request, 'question_list.html', context)


def question_details(request, pk):
    question = get_object_or_404(Question, id=pk)
    answers = Answer.objects.filter(question=pk).order_by('-added_at')
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            _ = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question.id})
    context = {
        'title': 'Question Page',
        'question': question,
        'answers': answers,
        'form': form,
    }
    return render(request, 'question_detail.html', context)


def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    context = {
        'title': 'Ask a Question',
        'form': form,
    }
    return render(request, 'ask_question.html', context)
