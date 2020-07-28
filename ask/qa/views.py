from django.http import HttpResponseRedirect, HttpResponseServerError
from .paginations import paginate
from django.shortcuts import render, get_object_or_404, reverse
from django.views.decorators.http import require_GET
from .models import Question, Answer
from .forms import AskForm, AnswerForm, SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .ajax import (HttpResponseAjax, HttpResponseAjaxError,
                   login_required_ajax)


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


@login_required(login_url='/login/')
def question_details(request, pk):
    question = get_object_or_404(Question, id=pk)
    is_liked = False
    if question.likes.filter(id=request.user.id).exists():
        is_liked = True
    answers = Answer.objects.filter(question=pk).order_by('-added_at')
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question.id})
    context = {
        'title': 'Question Page',
        'question': question,
        'answers': answers,
        'is_liked': is_liked,
        'form': form,
    }
    return render(request, 'question_detail.html', context)


@login_required(login_url='/login/')
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
    return render(request, 'base_form.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            form.save()
            user = authenticate(username=username,
                                password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('question_list'))
            else:
                return HttpResponseServerError()
    else:
        form = SignupForm()
    context = {
        'title': 'User registration',
        'form': form,
    }
    return render(request, 'base_form.html', context)


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,
                                password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('question_list'))
            else:
                form.add_error(None, 'The username or password you entered is incorrect')
    else:
        form = LoginForm()
    context = {
        'title': 'Sign in',
        'form': form,
    }
    return render(request, 'base_form.html', context)


def log_out(request):
    if request.user is not None:
        logout(request)
        return HttpResponseRedirect(reverse('question_list'))


@login_required_ajax
def like_question(request):
    question = get_object_or_404(Question, id=request.POST.get('question_id'))
    is_liked = False
    if question.likes.filter(id=request.user.id).exists():
        question.likes.remove(request.user)
        question.rating -= 1
        is_liked = False
        message = 'You disliked this question'
    else:
        question.likes.add(request.user)
        question.rating += 1
        is_liked = True
        message = 'You liked this question'
    question.save()
    if question:
        return HttpResponseAjax(message=message)
    else:
        return HttpResponseAjaxError(code='bad_params',
                                     message='Question does not exist',)
