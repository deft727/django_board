from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms.widgets import RadioSelect
from .models import *

class SignUpFormReader(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    of_age = forms.BooleanField(required=False)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['email'].label='Электороная почта'
        self.fields['confirm_password'].label='Подтвердите пароль'
        self.fields['of_age'].label = 'Есть 18?'
    class Meta:
            model = User
            fields=['username','email','password','confirm_password','of_age']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(f'Данный e-mail уже зарегистрован')
        return self.cleaned_data['email']


    def clean_username(self):
        username= self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} занято')
        return username

    def clean_of_age(self):
        of_age = self.cleaned_data['of_age']
        if not of_age:
            of_age = False
        else:
            of_age = True
        return of_age

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password= self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

class DateInput(forms.DateInput):
    input_type = 'date'

class SignUpFormBloger(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    birthday = forms.DateField(required=False, widget = DateInput())
    country = forms.CharField(max_length=50)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                widget=forms.CheckboxSelectMultiple)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label='Подтвердите пароль'
        self.fields['email'].label='Электороная почта'
        self.fields['country'].label='Город'
        self.fields['birthday'].label='Дата рождения'
        self.fields['category'].label='Категории'


    class Meta:
        model = User
        fields = ('username','email','password','confirm_password','birthday','country','category')
       

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(f'Данный e-mail уже зарегистрован')
        return self.cleaned_data['email']


    def clean_username(self):
        username= self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} занято')
        return username


    def clean(self):
        password = self.cleaned_data['password']
        confirm_password= self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data



class BlogerForm(forms.ModelForm):
    birthday = forms.DateField(required=False, widget = DateInput())
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Bloger
        fields = '__all__'
        exclude = ('user','bloger','is_super')






class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = '__all__'
        exclude = ('user','reader','is_super')