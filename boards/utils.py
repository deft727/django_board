from accounts.models import Bloger,Reader
from django.contrib.auth.models import User
from social_django import *
from social_core import *
from django.core.mail import send_mail
from django.contrib import messages
from .forms import *

def get_user_status(request):
    if request.user.is_authenticated:
        if Bloger.objects.filter(user=request.user).exists():
            bloger = 'True'
            return bloger
        else :
            bloger = 'False'
    else:
        bloger='False'
    return bloger 


def create_profile(strategy, details, response, user, *args, **kwargs):

    if Reader.objects.filter(user=user).exists():
        pass
    else:
        new_profile = Reader(user=user)
        new_profile.save()

    return kwargs


def send_user_mail(request,subject,content,email):
    try:
        mail=send_mail(subject, content,'test.blogodvich@gmail.com',[email,],
                     fail_silently=False)
        messages.success(request,'Письмо отправлено')
    except:
        messages.error(request,'Ошибка отправки')
