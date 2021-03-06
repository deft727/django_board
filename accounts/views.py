from django.contrib.auth import get_user, login as auth_login,authenticate
from django.http import request
from django.shortcuts import render, redirect,HttpResponseRedirect
from .forms import *
from .tasks import send_user_mail_task
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView,View,DetailView
from .models import *
from django.contrib import messages
from boards.urls import get_user_status
# import urllib
# import urllib.request as urllib2
# import json
from django.conf import settings
# from boards.utils import send_user_mail
from django.contrib import messages


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):

    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_form_class(self):
        if get_user_status(self.request) is True:
            self.form_class = BlogerForm
        else:
            self.form_class = ReaderForm
        return self.form_class

    def get_object(self):
        if get_user_status(self.request) is True:
            return Bloger.objects.get(user=self.request.user)
        else:
            return Reader.objects.get(user=self.request.user)
            
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.add_message(self.request,messages.SUCCESS,'account has been updated')
        return super().form_valid(form)



class ChooseSignup(View):
    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            return redirect('home')
        return render(request, 'choose_signup.html')


class RegistrationViewReader(View):

    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            return redirect('home')
        form= SignUpFormReader(request.POST or None)
        context = {
            'form':form,
            'title':'Sign up as reader'
        }
        return render(request,'signup.html',context)

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            form = SignUpFormReader(request.POST)
            if form.is_valid():
                new_user=form.save(commit=False)
                new_user.username=form.cleaned_data['username']
                new_user.email=form.cleaned_data['email']
                new_user.set_password(form.cleaned_data['password'])
                new_user.save()
                reader = Reader.objects.create(
                    user=new_user,
                    username=new_user.username,
                    of_age = form.cleaned_data['of_age']
                )
                reader.save()
                auth_login(request, new_user,  backend='django.contrib.auth.backends.ModelBackend')
                name  = form.cleaned_data['username'] if form.cleaned_data['username'] else 'Anonimous'
                send_user_mail_task.delay(subject='Hello Reader',content=f'Welcome on our site {name}',email=new_user.email)
                return redirect('home')
        else:
            form = SignUpFormReader()
        return render(request, 'signup.html', {'form': form})


class RegistrationViewBloger(View):

    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            return redirect('home')
        form= SignUpFormBloger(request.POST or None)
        context = {
            'form':form,
            'title':'Sign up as bloger',
        }
        return render(request,'signup.html',context)


    def post(self,request,backend='django.contrib.auth.backends.ModelBackend',*args,**kwargs):
        if request.method == 'POST':
            form = SignUpFormBloger(request.POST)
            if form.is_valid():

                new_bloger=form.save(commit=False)
                new_bloger.username=form.cleaned_data['username']
                new_bloger.email=form.cleaned_data['email']
                new_bloger.set_password(form.cleaned_data['password'])
                new_bloger.save()
                bloger = Bloger.objects.create(
                    user=new_bloger,
                    username=form.cleaned_data['username'],
                    email=new_bloger.email,
                    birthday = form.cleaned_data['birthday'],
                    country = form.cleaned_data['country'],
                    status = form.cleaned_data['status']
                )
                bloger.save()
                bloger.category.add(*form.cleaned_data['category'])
                auth_login(request, new_bloger,  backend='django.contrib.auth.backends.ModelBackend')
                name  = form.cleaned_data['username'] if form.cleaned_data['username'] else 'Anonimous'
                send_user_mail_task.delay(subject='Hello Bloger',content=f'Welcome on our site {name}',email=new_bloger.email)
                return redirect ('home')
        else:
            form = SignUpFormReader()
        return render(request, 'signup.html', {'form': form})


class LoginView(View):

    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            messages.add_message(request,messages.ERROR,'???? ?????? ????????????????????')
            return redirect('home')
        form = LoginForm(request.POST or None)
        title = 'Login'
        context= {'title':title,
        'form':form,
        }
        return render(request,'login.html',context)

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST or None)
        if form.is_valid():
           
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if '@' in username:
                user1= User.objects.filter(email=username).first()
                user= authenticate(username=user1,password=password)
            else:
                user= authenticate(username=username,password=password)
            if user:
                auth_login(request,user)
            return HttpResponseRedirect('/')
        context={'form':form,}
        return render(request,'login.html',context)



class ProfileView(DetailView):

    template_name='profile.html'
    allow_empty=False
    model= User

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        if self.get_object().bloger.get_queryset():
            profile = self.get_object().bloger.get_queryset()
            status = True
        else:
            profile = self.get_object().reader.get_queryset()
            status = False

        context['status'] = status
        context['profile'] = profile
        context['title'] = f'Profile {self.get_object().username}'
        return context
