from django.contrib.admin.options import VERTICAL
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True,verbose_name='Доска')
    description = models.CharField(max_length=100,verbose_name='Описание')

    class Meta:
        verbose_name ='Доска'
        verbose_name_plural ='Доски'

    def __str__(self):
        return self.name

    def get_posts_count(self):
       return Post.objects.filter(topic__board=self).count()

    def get_absolute_url(self):
        return reverse("board_topics",kwargs={"pk":self.pk})


class Topic(models.Model):
    subject = models.CharField(max_length=255,verbose_name='Тема')
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics',on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics',on_delete=models.CASCADE)

    class Meta:
        verbose_name ='Тема'
        verbose_name_plural ='Темы'

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000,help_text='Макс. кол-во символов 4000',verbose_name='Сообщение')
    topic = models.ForeignKey(Topic, related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts',on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+',on_delete=models.CASCADE)

    class Meta:
        verbose_name ='Пост'
        verbose_name_plural ='Посты'



    