from django.contrib.admin.options import VERTICAL
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown
from simple_history.models import HistoricalRecords
import math
import sys
from PIL import Image
import PIL
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import io
from django.core.files.base import ContentFile
from django.core.files import File


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True,verbose_name='Доска')
    description = models.CharField(max_length=100,verbose_name='Описание')
    history = HistoricalRecords()

    class Meta:
        verbose_name ='Доска'
        verbose_name_plural ='Доски'
        ordering = ['-pk',]

    def __str__(self):
        return self.name

    def get_posts_count(self):
       return Post.objects.filter(topic__board=self).count()

    def get_absolute_url(self):
        return reverse("board_topics",kwargs={"pk":self.pk})

    def get_last_post(self):
            return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True,null=True)
    file = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey("Topic",on_delete=models.CASCADE)




            # image1=self.file
            # if image1 :

            #     img1=Image.open(image1)
            #     new_img1=img1.convert('RGB')
            #     res_img1=new_img1.resize((1920,650),Image.ANTIALIAS)
            #     filestream= BytesIO()
            #     file_=res_img1.save(filestream,'JPEG',quality=90)
            #     filestream.seek(0)
            #     name= '{}.{}'.format(*self.image1.name.split('.'))
            #     self.image1 = InMemoryUploadedFile(
            #         filestream,'ImageFiedl',name,'jpeg/image',sys.getsizeof(filestream),  None
            #     )
            #     super().save(*args,**kwargs)

    # def save(self,*args,**kwargs):
    #     b = io.BytesIO()
    #     image = PIL.Image.open(self.file)
    #     image.save(b, format='PNG')
    #     b.seek(0)
    #     # b.save()
    #     super().save(*args,**kwargs)
        # file=self.file
        # if file :
        #     rawbytes = file
        #     im = Image.frombuffer("I;16", (5, 10), rawbytes, "raw", "I;12")
        #     im.save()
        #     super().save(*args,**kwargs)


class Topic(models.Model):
    # photo = models.ForeignKey(Photo,blank=True,on_delete=CASCADE)
    subject = models.CharField(max_length=255,verbose_name='Тема')
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board,on_delete=models.CASCADE)
    starter = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name ='Тема'
        verbose_name_plural ='Темы'
        
    def __str__(self):
        return self.subject

    def get_photo(self):
        return Photo.objects.filter(topic=self).first()

    def get_photos(self):
        return Photo.objects.filter(topic=self)[1:]

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)
        
    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]



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

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


    