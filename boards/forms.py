from django import forms
from .models import Topic,Post,Board

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'row':5,'placeholder':'what is your mind?'}
        ),
        max_length=4000,
        help_text='Max length is 4000')

    class Meta:
        model = Topic
        fields = ['subject', 'message']
    


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = '__all__'       