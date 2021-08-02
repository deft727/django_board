from django import forms
from django.http import request
from .models import Topic,Post,Board,Photo

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'row':5,'placeholder':'what is your mind?'}
        ),
        max_length=4000,
        help_text='Max length is 4000')
    file = forms.FileField(required=False)
    class Meta:
        model = Topic
        fields = ['subject', 'message','file']
    


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = '__all__'       


