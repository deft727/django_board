from django import forms
from django.forms import fields
from django.http import request
from .models import Topic,Post,Board,Photo

class NewTopicForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'row':5,'placeholder':'what is your mind?'}
        ),
        max_length=4000,
        help_text='Max length is 4000')
    # file = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))

    file = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={
        'multiple': True,
        'class':'js-upload-photos',
        'id':'fileupload',
        # 'style':'display: none',
        # 'data-url':"{% url 'new_topic' board.pk %}",
        # 'data-form-data':'{"csrfmiddlewaretoken": "{{ csrf_token }}"}'
        }))
    
    class Meta:
        fields =('subject','message','file')

# class NewPhotoForm(forms.Form):
#     file = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={
#         'multiple': True,
#         'class':'js-upload-photos',
#         'id':'fileupload',
#         # 'style':'display: none',
#         # 'data-url':"{% url 'new_topic' board.pk %}",
#         # 'data-form-data':'{"csrfmiddlewaretoken": "{{ csrf_token }}"}'
#         }))
#     # name = forms.CharField(required=False)


    



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = '__all__'       


