from django import forms
from django.forms import ModelForm
from .models import Post

class Postform(ModelForm):
    class Meta:
        model = Post
        fields = ('post',)

        labels={
            'post':"",
        }

        widgets ={
            'post' : forms.Textarea(attrs={'placeholder': "What's happening ?",'cols': 110, 'rows': 1 ,'class': 'inputfield'}),
        }