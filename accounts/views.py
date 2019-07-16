from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.conf import settings


def signup(request):
    if request.method == "POST":
        # form = UserCreationForm(request.POST)
        form = SignupForm(request.POST)
        if form.is_valid():
            # user = form.save()
            form.signup()
            return redirect(settings.LOGIN_URL)
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {
        'form': form
    })