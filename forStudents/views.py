# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from audioop import reverse

from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


from forStudents.models import Question, Choice, Tests


@login_required(login_url='/accounts/login/')
def index(request):
    latest_tests_list = Tests.objects.all()
    context = {'latest_tests_list': latest_tests_list}
    # from django.contrib.auth import authenticate
    # user = authenticate(username='kirillsaltykov', password='Kirill1994!')
    # if user is not None:
    #     # the password verified for the user
    #     if user.is_active:
    #         print("User is valid, active and authenticated")
    #     else:
    #         return render(request, 'forStudents/registration/login.html')
    # else:
    #     # the authentication system was unable to verify the username and password
    #     print("The username and password were incorrect.")
    #     return render(request, 'forStudents/registration/login.html')
    return render(request, 'forStudents/index.html', context)

def question_of_test(request, test_id):
    for votes in Choice.objects.filter(votes=True):
        votes.votes=False
        votes.save()
    latest_question_list = Question.objects.filter(parent_test=test_id)
    template = loader.get_template('forStudents/question_of_test.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'forStudents/question_of_test.html', context)



def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
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
        # Redisplay the question voting form.
        return render(request, 'forStudents/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        latest_question_list = Question.objects.filter(parent_test=question.parent_test).order_by('-pub_date')[:5]
#        if question.number< max(Question.objects.values('number')).get('number'):
        if question.number < max(latest_question_list.values('number')).get('number'):

            return render(request, 'forStudents/detail.html',
                          {'question': get_object_or_404(Question, number=question.number+1)}) #Question.objects.filter(number=question.number+1)})
        #return HttpResponseRedirect(reverse('forStudents:results', args=(question.id,)))
    #    latest_question_list = Question.objects.order_by('-pub_date')[:5]

        truelist = Choice.objects.filter(question__in=latest_question_list.values('id'), votes=True)
        score = 0
        for i in truelist:
            score = score+i.score
        return render(request, 'forStudents/results.html', {'question': question,
                                                            'latest_question_list': latest_question_list, 'truelist':truelist, 'truecol':truelist,
                                                            'truecol':len(truelist), 'score':score})
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            render(request, 'forStudents/start/')
        else:
            print ('tut nashi polnomochia vse')
    else:  print ('tut nashi polnomochia vse')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def logout_view(request):
    logout(request)