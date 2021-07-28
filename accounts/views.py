from django.contrib.auth import get_user, login as auth_login
from django.http import request
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView,View
from .models import *
from django.contrib import messages
from boards.urls import get_user

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):

    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')


    def get_form_class(self):
        if get_user(self.request) == 'bloger':
            self.form_class = BlogerForm
        else:
            self.form_class = ReaderForm
        return self.form_class


    def get_object(self):
        try:
            return Bloger.objects.get(user=self.request.user)
        except :
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
                auth_login(request, new_user)
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

    def post(self,request,*args,**kwargs):
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
                    email=new_bloger.email,
                    birthday = form.cleaned_data['birthday'],
                    country = form.cleaned_data['country'],
                )
                bloger.save()
                bloger.category.add(*form.cleaned_data['category'])

                auth_login(request,new_bloger)

                return redirect('home')
        else:
            form = SignUpFormReader()
        return render(request, 'signup.html', {'form': form})