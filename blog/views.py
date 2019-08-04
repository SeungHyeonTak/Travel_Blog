from django.shortcuts import render, get_object_or_404, redirect
from .models import About
from .forms import AboutForm
from django.contrib.auth.decorators import login_required


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


def about_detail(request, pk):
    about_details = get_object_or_404(About, pk=pk)
    return render(request, 'blog/about_detail.html', {
        'about_details': about_details,
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
    return render(request, 'blog/map_restaurant.html')


def hotplace(request):
    return render(request, 'blog/map_hotplace.html')
