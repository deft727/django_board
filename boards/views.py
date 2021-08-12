from datetime import date
from decimal import ROUND_UP
from math import e
import time
from django.db.models.expressions import F
# from django.http.response import HttpResponseRedirect
# from django.utils.translation import pgettext
# from xlwt.ExcelMagic import PtgNames
# from accounts.models import Bloger,Reader
# from os import name
from django.core.checks import messages
from django.urls.conf import path
from .forms import NewTopicForm,PostForm,BoardForm
from django.shortcuts import render, get_object_or_404,redirect
# from django.http import Http404, request
from django.db.models import Count
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import HttpResponse
from .models import Board, Photo, Topic , Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import View,ListView,UpdateView
from django.urls import reverse_lazy,reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login
from django.template.loader import render_to_string
from django.http import JsonResponse
from .utils import get_user_status,get_image
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models.signals import post_save
from accounts.tasks import send_user_mail_task
from django.dispatch import receiver
from django.db import transaction

import json





def new_articles(request):
    import random
    randomboard = ['Python','Django','Flask','Docker']
    randomname = ['Boris','Kirill','Sasha','Yura','Nikita']
    # if  request.user.is_authenticated:
    user = request.user
    # else:
    #     try:
    #         user =  User.objects.create_user(random.choice(randomname), 'randomemail', 'randomemail')
    #         login(request,user)
    #     except:
    #         user = User.objects.filter(username=randomname).first()
    try:
        board = Board.objects.get(name=random.choice(randomboard))
    except:
        board = Board.objects.create(name=random.choice(randomboard),description='dfsdfsd')

    for i in range(100):
        subject = 'Topic test #{}'.format(i)
        topic = Topic.objects.create(subject=subject, board=board, starter=user)
        Post.objects.create(message='Lorem ipsum...', topic=topic, created_by=user)
    return redirect('home')


# @login_required
# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     if request.method == 'POST':
#         form = NewTopicForm(request.POST,  request.FILES)
#         if form.is_valid():
#             topic = form.save(commit=False)
#             topic.board = board
#             topic.starter = request.user
#             topic.save()
#             post = Post.objects.create(
#                 message = form.cleaned_data.get('message'),
#                 topic = topic,
#                 created_by = request.user
#             )
#             photo = Photo.objects.create(
#                 file = form.cleaned_data.get('file'),
#                 topic = topic
#             )
#             photo.save()
#             href = 'true'
#             data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url,}  
#         else:
#             form = NewTopicForm()
#             data = {'is_valid': False}
            
#     return render(request, 'new_topic.html', {'board': board,'form':form})

# def photo_delete(request, pk):
#     board = get_object_or_404(Photo, pk=pk)
#     data = dict()
#     boards = Board.objects.all()
#     form1 = NewTopicForm(request.POST,request.FILES)

#     if request.method == 'POST':
#         board.delete()
#         data['form_is_valid'] = True
#         data['html_partial_board'] = render_to_string('new_topic.html',  'new_topic.html', {'board': board,'form':form1,'photos':None})
#     else:
#         context = {'board': board}
#         data['html_form'] = render_to_string('./includes/board_form_delete.html',
#             context,
#             request=request,
#         )
#     return JsonResponse(data)

@method_decorator(login_required, name='dispatch')
class New_topicView(View):

    def get(self,request,pk):
        board = get_object_or_404(Board, pk=pk)
        form1 = NewTopicForm(request.POST,request.FILES)
        return render(request, 'new_topic.html', {'board': board,'form':form1,'photos':None})

    @transaction.atomic
    def post(self,request,pk,images=[]):
        time.sleep(1)
        board = get_object_or_404(Board, pk=pk)
        form = NewTopicForm(request.POST,request.FILES)
        if form.is_valid():
            if not Topic.objects.filter(subject=form.cleaned_data.get('subject'),board=board):
                topic = Topic.objects.create(
                    subject=form.cleaned_data.get('subject'),
                    starter= request.user,
                    board = board
                )
                Post.objects.create(
                    message = form.cleaned_data.get('message'),
                    created_by=request.user,
                    topic=topic
                  )
            else:
                topic = Topic.objects.get(subject=form.cleaned_data.get('subject'),board=board)
            files =  request.FILES.getlist('file')
            
            for file in images if not files else files:
                photo = Photo(
                        title = file.name,
                        file = file,
                        topic = topic
                    )
                photo.save()
                data = {'is_valid': True, 'name': photo.title }

            if not files:
                return redirect('board_topics', pk=pk)
        else:
            photo = request.FILES.get('file')
            images.append(get_image(photo))
            data = {'is_valid': True, 'name': photo.name }
        return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class Reply_topicView(View):
    
    def get(self,request, pk, topic_pk):
        topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
        form = PostForm()
        context = {
            'topic':topic,
            'form':form,  
        }
        return render(request, 'reply_topic.html',context)

    def post(self,request, pk, topic_pk):
        topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
        form = PostForm(request.POST)
        if form.is_valid():

            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = timezone.now()
            topic.save()
            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            page = topic.get_page_count()
            topic_post_url = f'{topic_url}?page={page}'
            return redirect(topic_post_url)

        else:
            context = {
            'topic':topic,
            'form':form,}
            return render(request, 'reply_topic.html',context)



# @login_required
# def reply_topic(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.topic = topic
#             post.created_by = request.user
#             post.save()
#             topic.last_updated = timezone.now()
#             topic.save()
#             topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
#             page = topic.get_page_count()
#             topic_post_url = f'{topic_url}?page={page}'
#             return redirect(topic_post_url)
            
#     else:
#         form = PostForm()
#     return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'
    paginate_by = 10
    ordering= ['-id']
    def get_context_data(self,**kwargs):
        # messages.add_message(self.request,messages.SUCCESS,'khftyde')
        context = super().get_context_data(**kwargs)
        context['bloger'] = get_user_status(self.request)
        context['history'] = Board.history.all()[:10]
        context['boards'] = Board.objects.filter(is_activ=True).prefetch_related('topic_set')
        return context



class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topic_set.all().order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset
        

def generate_fake_data(request):
    from model_mommy import mommy
    mommy.make('boards.TOPIC', _quantity=20)
    return redirect('boards')


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)
        
    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


@login_required
def board_create(request):
    data = dict()
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            boards = Board.objects.all()
            data['html_partial_board'] = render_to_string('./includes/partial_board.html', {
                'boards': boards,
                'bloger': get_user_status(request)
                })
        else:
            data['form_is_valid'] = False
    else:
        form = BoardForm()

    context = {'form': form}
    data['html_form'] = render_to_string('./includes/board_form.html',
        context,
        request=request
    )
    return JsonResponse(data)


@login_required
def board_update(request,pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
    else:
        form = BoardForm(instance=board)
    return save_board_form(request, form, './includes/board_form_update.html')


def save_board_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            boards = Board.objects.all()
            data['html_partial_board'] = render_to_string('./includes/partial_board.html', {
                'boards': boards,
                'bloger': get_user_status(request)
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def board_delete(request, pk):
    board = get_object_or_404(Board, pk=pk)
    data = dict()
    boards = Board.objects.all()
     
    if request.method == 'POST':
        board.delete()
        data['form_is_valid'] = True
        data['html_partial_board'] = render_to_string('./includes/partial_board.html', {
            'boards': boards,
            'bloger': get_user_status(request),
            # 'messages': messages.add_message(request,messages.SUCCESS,'добавлен')
        })

    else:
        context = {'board': board}
        data['html_form'] = render_to_string('./includes/board_form_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)



