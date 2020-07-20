from django import forms
from .models import Question, Answer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class AskForm(forms.Form):
    title = forms.CharField(max_length=1024)
    text = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.strip() == '':
            raise forms.ValidationError('Title field cannot be empty', code='validation_error')
        return title

    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '':
            raise forms.ValidationError('Text field cannot be empty', code='validation_error')
        return text

    def clean(self):
        return self.cleaned_data

    def save(self):
        question = Question(**self.cleaned_data)
        question.author = self._user
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '':
            raise forms.ValidationError('Text field cannot be empty', code='validation_error')
        return text

    def clean_question(self):
        question_id = self.cleaned_data['question']
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            question = None
        return question

    def clean(self):
        return self.cleaned_data

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author = self._user
        answer.save()
        return answer


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('Username field cannot be empty', code='validation_error')
        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with the same username already exists', code='validation_error')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.strip() == '':
            raise forms.ValidationError('Email field cannot be empty', code='validation_error')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('Password field cannot be empty', code='validation_error')
        self.raw_password = password
        return make_password(password)

    def save(self):
        user = User(**self.cleaned_data)
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Username not specified')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Password not specified')
        return password

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('The username or password you entered is incorrect')
        if not user.check_password(password):
            raise forms.ValidationError('The username or password you entered is incorrect')
