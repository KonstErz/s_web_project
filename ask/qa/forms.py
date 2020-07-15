from django import forms
from .models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=1024, help_text='Enter the name (title) of your question')
    text = forms.CharField(widget=forms.Textarea, help_text='Enter the text of your question')

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

    def save(self):
        question = Question(**self.cleaned_data)
        question.author = self._user
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, help_text='Enter the text of your answer')
    question = forms.IntegerField(widget=forms.HiddenInput, help_text='Enter Question ID')

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
            raise forms.ValidationError('The question with this id does not exist', code='validation_error')
        return question

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author = self._user
        answer.save()
        return answer
