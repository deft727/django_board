from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms.widgets import RadioSelect
from django.urls.conf import path
from .models import *
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
class SignUpFormReader(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    of_age = forms.BooleanField(required=False)
    interests = forms.ModelMultipleChoiceField(queryset=Interests.objects.all(),
                                                widget=forms.CheckboxSelectMultiple,
                                                required=False)
    captcha = ReCaptchaField(widget=ReCaptchaWidget())

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['email'].label='Электороная почта'
        self.fields['confirm_password'].label='Подтвердите пароль'
        self.fields['of_age'].label = 'Есть 18?'
        self.fields['interests'].label='Интересы'

    class Meta:
            model = User
            fields=['username','email','password','confirm_password','of_age','interests','captcha']

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
    STATUS_TRUE ='True'
    STATUS_FALSE='False'

    STATUS_CHOICES= (
        (STATUS_TRUE,'bloger'),
        (STATUS_FALSE,'isn`t bloger'),
    )

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    birthday = forms.DateField(required=False, widget = DateInput())
    country = forms.CharField(max_length=50)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                widget=forms.CheckboxSelectMultiple,
                                                required=False)
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False
    )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label='Подтвердите пароль'
        self.fields['email'].label='Электороная почта'
        self.fields['country'].label='Город'
        self.fields['birthday'].label='Дата рождения'
        self.fields['category'].label='Категории'
        self.fields['status'].label='status'


    class Meta:
        model = User
        fields = ('username','email','password','confirm_password','birthday','country','category','status','captcha')
       

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
        exclude = ('user','bloger','is_super',)


class ReaderForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(queryset=Interests.objects.all(),
                                                widget=forms.CheckboxSelectMultiple,
                                                required=False)
    class Meta:
        model = Reader
        fields = '__all__'
        exclude = ('user','reader','is_super')



class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaWidget())


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Логин или е-майл'
        self.fields['password'].label = 'Пароль'
        
    def clean(self):
        username= self.cleaned_data['username']
        password= self.cleaned_data['password']

        if '@' in username:
            if not User.objects.filter(email=username).exists():
                raise forms.ValidationError(f'Пользователь с  почтой  {username} не найден.')
        else:
            if not User.objects.filter(username=username).exists():
                raise forms.ValidationError(f'Пользователь с логином   {username} не найден.')

        user = User.objects.filter(username=username).first()
        user1= User.objects.filter(email=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Неверный пароль")
        else:
            if not user1.check_password(password):
                raise forms.ValidationError("Неверный пароль")

        return self.cleaned_data

    class Meta:
        model=User
        fields= ['username','password','captcha']






# class SignUpForm(UserCreationForm):
#     email = forms.CharField(max_length=254, required=False, widget=forms.EmailInput())

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')