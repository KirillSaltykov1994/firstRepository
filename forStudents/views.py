# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from forStudents.models import Question, Choice, Tests, Tryes


@login_required(login_url='/accounts/login/')
def index(request):
    latest_tests_list = Tests.objects.all()
    context = {'latest_tests_list': latest_tests_list}
    return render(request, 'forStudents/index.html', context)


def question_of_test(request, test_id):
    for votes in Choice.objects.filter(votes=True):
        votes.votes = False
        votes.save()
    latest_question_list = Question.objects.filter(parent_test=test_id).order_by('number')
    template = loader.get_template('forStudents/question_of_test.html')
    try:
        tryes = Tryes.objects.get(user=request.user, test__id=test_id)
    except:
        tryes = Tryes(user=request.user, test=Tests.objects.get(id=test_id), count=0)
        tryes.save()
    if tryes.count < 3:
        context = {
            'latest_question_list': latest_question_list,
        }
        return render(request, 'forStudents/question_of_test.html', context)
    else:
        context = {
            'fail': u'Больше нельзя проходить этот тест',
        }
        return render(request, 'forStudents/question_of_test.html', context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Вопросы не созданы")
    return render(request, 'forStudents/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'forStudents/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        selected_choice.votes = True
        selected_choice.save()
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'forStudents/detail.html', {
            'question': question,
            'error_message': "Требуется ответ на вопрос",
        })
    else:
        latest_question_list = Question.objects.filter(parent_test=question.parent_test).order_by('-pub_date')[:5]
        #        if question.number< max(Question.objects.values('number')).get('number'):
        if question.number < max(latest_question_list.values('number')).get('number'):
            return render(request, 'forStudents/detail.html',
                          {'question': get_object_or_404(Question,
                                                         number=question.number + 1)})

        truelist = Choice.objects.filter(question__in=latest_question_list.values('id'), votes=True)
        score = 0
        for i in truelist:
            score = score + i.score
        if score > Tests.objects.get(id=question.parent_test.id).limit:
            res = 'Тест пройден'
        else:
            res = 'Тест провален'
        tryes = Tryes.objects.get(user=request.user, test__id=question.parent_test.id)
        tryes.count = tryes.count + 1
        tryes.save()
        return render(request, 'forStudents/results.html', {'question': question,
                                                            'latest_question_list': latest_question_list,
                                                            'truelist': truelist, 'truecol': truelist,
                                                            'truecol': len(truelist), 'score': score,
                                                            'tryes': tryes.count, 'res': res})


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            render(request, 'forStudents/start/')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'forStudents/signup.html'


def logout_view(request):
    logout(request)
