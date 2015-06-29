# coding=utf-8
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login

class LoginForm(forms.Form):
    login = forms.CharField(label=u'Логин')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput)

    def execute(self, request):
        cd = self.cleaned_data
        user = authenticate(username=cd['login'], password=cd['password'])
        if user is not None:
            if not user.is_active:
                messages.error(request, u'Пользователь не активен')
            else:
                login(request, user)
        else:
            messages.error(request, u'Пользователь с таким логином и паролем не найден')