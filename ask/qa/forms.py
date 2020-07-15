from django import forms
from .models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=1024)
    text = forms.CharField(widget=forms.Textarea)
    author = forms.IntegerField(widget=forms.HiddenInput)

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
        self.cleaned_data['author'] = self._user
        return Question.objects.create(**self.cleaned_data)


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)
    author = forms.IntegerField(widget=forms.HiddenInput)

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
        self.cleaned_data['author'] = self._user
        return Answer.objects.create(**self.cleaned_data)
