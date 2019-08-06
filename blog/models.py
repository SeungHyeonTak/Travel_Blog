from django.db import models
from django.conf import settings
from django import forms
from django.urls import reverse
from django.utils import timezone

User = settings.AUTH_USER_MODEL


def min_length_3_valudator(value):
    if len(value) < 3:
        raise forms.ValidationError('3글자 이상 입력해주세요.')


class About(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='About')  # 사용자
    title = models.CharField(max_length=50, validators=[min_length_3_valudator])  # 제목
    country = models.CharField(max_length=50, help_text='국가를 입력하세요')# 나라
    city = models.CharField(max_length=50, help_text='도시를 입력하세요')# 도시
    content = models.TextField(blank=True)  # 내용
    photo = models.ImageField(blank=True, upload_to='blog/image/%Y/%m/%d')  # 사진
    post_hit = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)  # 작성 날짜
    updated = models.DateTimeField(auto_now=True)  # 수정 날짜

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:about_detail', args=[self.id])

    # @property
    # def update_counter(self):
    #     self.post_hit = self.post_hit + 1
    #     self.save()

    # def get_absolute_url(self):
    #     return reversed('')


# 게시글 조회 기록 저장
# class HitCount(models.Model):
#     ip = models.CharField(max_length=20, default=None, null=True) # ip 주소
#     post = models.ForeignKey(About, on_delete=models.CASCADE, default=None, null=True) # 게시글
#     date = models.DateTimeField(default=timezone.now(), null=True, blank=True) # 조회수가 올라갔던 날짜

class Comment(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.author.username if self.author else "무명") + "의 댓글"

    class Meta:
        ordering = ['-id']

    # def get_edit_url(self):
    #     return reverse('blog:comment_edit', args=[self.about.pk, self.pk])
    #
    # def get_delete_url(self):
    #     return reverse('blog:comment_delete', args=[self.about.pk, self.pk])
