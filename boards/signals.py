from django import contrib
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import request
from accounts.tasks import send_user_mail_task
from .models import Post, Topic
from django.db.models import Count



@receiver(post_save, sender=Post)
def reply_topic(sender, instance, **kwargs):
    countable = instance.topic.board.topic_set.all().annotate(replies=Count('posts') - 1)
    # print(countable[0].replies)
    if countable[0].replies >= 1:
        email = instance.topic.starter.email
        topic_name = instance.topic.subject
        topic_user = instance.created_by
        send_user_mail_task.delay(subject=f' replayed topic {topic_name }',
                    content= f' "{topic_user}" replayed your topic "{topic_name}" ',email=email)