from django import forms
from .models import Post, Category, User

class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', widget=forms.Select(attrs={'class': 'input is-medium'}))
    author = forms.ModelChoiceField(queryset=User.objects.all(), label='Автор', widget=forms.Select(attrs={'class': 'input is-medium'}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'author']

