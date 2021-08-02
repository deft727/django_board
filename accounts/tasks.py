from celery import shared_task
from django.core.mail import send_mail
from myproject.celery import app



@shared_task
def add(x, y):
    return x + y


@app.task
def send_user_mail_task(subject,content,email):
    send_mail(subject, content,'test.blogodvich@gmail.com',[email,],
                     fail_silently=False)


@shared_task
def xsum(numbers):
    return sum(numbers)



