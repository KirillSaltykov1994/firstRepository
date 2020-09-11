from django.conf.urls import  url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView, RedirectView

from . import views
from .views import SignUpView

app_name = 'forStudents'
urlpatterns = [
    # ex: /polls/
    # ex: /polls/5/
#    url(r'^index2/(\d+)', TemplateView.as_view(template_name='index.html'), name='index'),

 #   url(r'^index/(\d+)', views.index2, name='index'),

    # ex: /polls/5/results/
    url(r'^/results/', views.results, name='results'),

    url(r'^test/(\d+)', views.question_of_test, name='question_of_test'),
    # ex: /polls/5/vote/
    url(r'^(\d+)/vote/', views.vote, name='vote'),

    url(r'^(\d+)/detail', views.detail, name='detail'),

#    url('login/', views.login, name='login'),
    url('signup/', SignUpView.as_view(), name='signup'),
    url(r'', views.index, name='index'),
]