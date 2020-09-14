# -*- coding: utf-8 -*-
from django import forms

from .models import Tests, Question


class PostForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question_text',)
    question_text = forms.RadioSelect()