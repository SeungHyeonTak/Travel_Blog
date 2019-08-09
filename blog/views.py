import math
import json
import googlemaps
import folium
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import AboutForm, CommentForm
from django.contrib.auth.decorators import login_required
from secret import *
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.template.loader import render_to_string
from hitcount.views import HitCountDetailView

User = get_user_model()


class PostCountHitDetailView(HitCountDetailView):
    model = Post_count
    count_hit = True


def main_list(request):
    return render(request, 'blog/main.html')


def about(request):
    abouts = About.objects.all()
    page = int(request.GET.get('page', 1))  # page 부분 세팅 하기
    paginated_by = 6
    total_count = len(abouts)
    total_page = math.ceil(total_count / paginated_by)
    page_range = range(1, total_page + 1)
    start_index = paginated_by * (page - 1)
    end_index = paginated_by * page
    abouts = abouts[start_index:end_index]
    return render(request, 'blog/about.html', {
        'abouts': abouts,
        'total_page': total_page,
        'page_range': page_range,
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
    return render(request, 'blog/about_new.html', {
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
    # form = AboutForm()
    # abouts = about_details.comments
    comment_form = CommentForm()
    comments = about_details.comments.all()
    return render(request, 'blog/about_detail.html', {
        'about_details': about_details,
        'comment_form': comment_form,
        'comments': comments,
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


def comment_create(request, pk):
    is_ajax = request.POST.get('is_ajax')

    about = get_object_or_404(About, pk=pk)
    comment_form = CommentForm(request.POST)
    comment_form.instance.author_id = request.user.id
    comment_form.instance.about_id = pk
    if comment_form.is_valid():
        comment = comment_form.save()

    if is_ajax:
        html = render_to_string('blog/comment_single.html', {
            'comment': comment,
        })
        return JsonResponse({'html': html})
    return redirect(about)


def comment_update(request, comment_pk):
    is_ajax, data = (request.GET.get('is_ajax'), request.GET) if 'is_ajax' in request.GET else (
        request.POST.get('is_ajax', False), request.POST)

    comment = get_object_or_404(Comment, pk=comment_pk)
    about = get_object_or_404(About, pk=comment.about.id)  # ??

    if request.user != comment.author:
        messages.warning(request, '권한없음')
        return redirect(about)

    if is_ajax:
        form = CommentForm(data, instance=comment)
        if form.is_valid():
            form.save()
            return JsonResponse({'works': True})
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(about)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_update.html', {
        'form': form,
    })


def comment_delete(request, comment_pk):
    is_ajax = request.GET.get('is_ajax') if 'is_ajax' in request.GET else request.POST.get('is_ajax', False)
    comment = get_object_or_404(Comment, pk=comment_pk)
    about = get_object_or_404(About, pk=comment.about.id)

    # if request.user != comment.author and not request.user.is_staff and request.user != about.author:
    if comment.author != User.objects.get(username=request.user.get_username()):
        messages.warning(request, '권한 없음')
        return redirect(about)

    if is_ajax:
        comment.delete()
        return JsonResponse({'works': True})

    if request.method == "POST":
        comment.delete()
        return redirect(about)
    else:
        return render(request, 'blog/comment_delete.html', {'object': comment})


def restaurant(request):
    res_list = Maplocation.objects.all()
    with open('loca.json', 'rt', encoding='utf8') as f:
        json_string = f.read()
        res = json.loads(json_string)

    return render(request, 'blog/map_restaurant.html', {
        'naver_api': naver_api,
        'res_list': res_list,
        'res': res,
    })


def hotplace(request):
    return render(request, 'blog/map_hotplace.html', {
        'naver_api': naver_api,
    })
