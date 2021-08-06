from PIL.Image import blend
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT
from django.urls import reverse
from django import forms


class Interests(models.Model):
    class Meta:
        verbose_name = 'Интерес'
        verbose_name_plural = 'Интересы'
        ordering = ['title',]

    title = models.CharField(max_length=250,verbose_name='Интерес')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('interests',kwargs={'slug':self.slug})

    def __str__(self):
        return self.title


class Category(models.Model):
    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['name',]

    name = models.CharField(max_length=250,verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})

    def __str__(self):
        return self.name


class Bloger(models.Model):
    class Meta:
        verbose_name = 'Блогер'
        verbose_name_plural = 'Блогеры'

    STATUS_TRUE ='True'
    STATUS_FALSE='False'

    STATUS_CHOICES= (
        (STATUS_TRUE,'bloger'),
        (STATUS_FALSE,'isn`t bloger'),
    )
    file = models.ImageField(null=True,blank=True)
    category = models.ManyToManyField(Category,verbose_name='Категории')
    user = models.ForeignKey(User, verbose_name='блогер', on_delete=models.CASCADE,related_name='bloger')
    username = models.CharField(blank=True, null=True, default=None, max_length=255,  verbose_name='имя')
    email = models .EmailField(verbose_name='Электороная почта')
    birthday = models.DateField(null=True, blank=True,verbose_name='Дата рождения')
    country = models.CharField(null=True, blank=True, default=None, max_length=255,  verbose_name='Город')
    is_super = models.BooleanField(default=True)
    status = models.CharField(
        max_length=100,
        verbose_name='are you bloger?',
        choices=STATUS_CHOICES,
        default=STATUS_TRUE
    )


class Reader(models.Model):
    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'
        
    file = models.ImageField(null=True,blank=True)
    user = models.ForeignKey(User, verbose_name='читатель', on_delete=models.CASCADE)
    username = models.CharField(blank=True, null=True,  max_length=50,  verbose_name='имя')
    is_super = models.BooleanField(default=False)
    of_age = models.BooleanField(default=False,null=True,blank=True)
    interests = models.ManyToManyField(Interests,verbose_name='Интересы')


# class Avatar(models.Model):
#     avatar = models.ImageField(upload_to='image/')
#     user = models.OneToOneField(User,on_delete=PROTECT)
# class AvatarForm(forms.ModelForm):
#     x = forms.FloatField(widget=forms.HiddenInput())
#     y = forms.FloatField(widget=forms.HiddenInput())
#     width = forms.FloatField(widget=forms.HiddenInput())
#     height = forms.FloatField(widget=forms.HiddenInput())

#     class Meta:
#         model = Avatar
#         fields = ('file', 'x', 'y', 'width', 'height', )


#     def save(self):
#         avatar = super(AvatarForm, self).save()

#         x = self.cleaned_data.get('x')
#         y = self.cleaned_data.get('y')
#         w = self.cleaned_data.get('width')
#         h = self.cleaned_data.get('height')

#         image = Image.open(avatar.file)
#         cropped_image = image.crop((x, y, w+x, h+y))
#         resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
#         resized_image.save(avatar.file.path)

#         return avatar
