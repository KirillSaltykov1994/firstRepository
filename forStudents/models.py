# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Tests(models.Model):
    nameOfTest = models.CharField(max_length=250)

    def __str__(self):
        return self.nameOfTest


class Tryes(models.Model):
    user = models.ForeignKey(User)
    test = models.ForeignKey(Tests)
    count = models.IntegerField(default=0)

class Question(models.Model):
    parent_test = models.ForeignKey(Tests, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    number = models.IntegerField()

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.BooleanField(default=False)
    right = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
