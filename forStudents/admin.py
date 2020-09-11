# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Question, Choice, Tests

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Tests)