from accounts.models import Bloger,Reader
# from django.contrib.auth.models import User
from social_django import *
from social_core import *
from .forms import *
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from io import BytesIO


def get_image(photo):
        img3=Image.open(photo)
        new_img3=img3.convert('RGB')
        res_img3=new_img3.resize((700,450),Image.ANTIALIAS)
        filestream= BytesIO()
        file_=res_img3.save(filestream,'JPEG',quality=90)
        filestream.seek(0)
        name= '{}.{}'.format(*photo.name.split('.'))
        photo = InMemoryUploadedFile(
            filestream,'ImageFiedl',name,'jpeg/image',sys.getsizeof(filestream),  None
        )
        return photo


def get_user_status(request):
    if request.user.is_authenticated:
        if Bloger.objects.filter(user=request.user).exists():
            bloger = True
            return bloger
        else :
            bloger = False
    else:
        bloger= False
    return bloger


def create_profile(strategy, details, response, user, *args, **kwargs):

    if Reader.objects.filter(user=user).exists():
        pass
    else:
        new_profile = Reader(user=user)
        new_profile.save()

    return kwargs


# def send_user_mail(request,subject,content,email):
#     try:
#         mail=send_mail(subject, content,'test.blogodvich@gmail.com',[email,],
#                      fail_silently=False)
#         messages.success(request,'Письмо отправлено')
#     except:
#         messages.error(request,'Ошибка отправки')
