from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import About
from .forms import AboutForm
from django.contrib.auth.decorators import login_required
from secret import *
from django.contrib.auth import get_user_model
import json

User = get_user_model()


def main_list(request):
    return render(request, 'blog/main.html')


def about(request):
    abouts = About.objects.all()
    return render(request, 'blog/about.html', {
        'abouts': abouts,
    })


@login_required
def about_new(request):
    if request.method == "POST":
        form = AboutForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            form.save()
            return redirect('blog:about')
    else:
        form = AboutForm()
    return render(request, 'blog/about_new.html', {  # 모달로 로그인 하라고 띄워주기나 로그인 페이지로 ㄱㄱ
        'form': form,
    })


def about_update(request, pk):
    if request.method == "POST":
        about = get_object_or_404(About, pk=pk)
        form = AboutForm(request.POST, request.FILES, instance=about)
        if form.is_valid():
            form.save()
            return redirect('blog:about')
    else:
        about = get_object_or_404(About, pk=pk)
        form = AboutForm(instance=about)

    return render(request, 'blog/about_update.html', {
        'form': form,
    })


def about_detail(request, pk):
    about_details = get_object_or_404(About, pk=pk)
    form = AboutForm()
    # abouts = about_details.comments
    return render(request, 'blog/about_detail.html', {
        'about_details': about_details,
        'form': form,
    })


# 게시물 삭제
def about_delete(request, pk):
    about = get_object_or_404(About, pk=pk)
    if request.method == "POST":
        about.delete()
        return redirect('blog:about')
    return render(request, 'blog/about_delete.html', {
        'about': about,
    })


# @login_required
def comment_new(request, about_pk):
    abouts = get_object_or_404(About, pk=about_pk)

    if request.method == "POST":
        form = AboutForm(request.POST, request.FILES)
        if form.is_valid():
            qs = form.save(commit=False)
            qs.about = about
            qs.author = request.uesr
            qs.save()
            return redirect('blog:about_detail', about.pk)
    else:
        form = AboutForm()

    return render(request, 'blog/about_new.html', {
        'form': form
    })


def restaurant(request):
    with open('loca.json', 'rt', encoding='utf8') as f:
        json_string = f.read()
        res = json.loads(json_string)
    return render(request, 'blog/map_restaurant.html', {
        'naver_api': naver_api,
        'res': res,
    })


def hotplace(request):
    return render(request, 'blog/map_hotplace.html', {
        'naver_api': naver_api,
    })
