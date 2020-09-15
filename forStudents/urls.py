from django.conf.urls import  url
from . import views
from .views import SignUpView

app_name = 'forStudents'
urlpatterns = [
    url(r'^/results/', views.results, name='results'),
    url(r'^test/(\d+)', views.question_of_test, name='question_of_test'),
    url(r'^(\d+)/vote/', views.vote, name='vote'),
    url(r'^(\d+)/detail', views.detail, name='detail'),
    url('signup', SignUpView.as_view(), name='signup'),
    url(r'', views.index, name='index'),
]