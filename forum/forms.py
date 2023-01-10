from django import forms
from django.contrib.auth.models import User

from .models import Comment, Post, Profile


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'tags',
        ]
        labels = {
            'title': 'タイトル',
            'content': '内容',
            'tags': 'タグ',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['tags'].widget.attrs.update({
            'data-role': 'tagsinput',
            'class': 'form-control',
        })
        self.fields['tags'].help_text = '\
            </br><span class="text-muted">複数タグはカンマ区切りかエンター区切り</span>'


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        max_length=1000,
        required=True,
        label='',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 5, 'width': 'auto'}
        )
    )

    class Meta:
        model = Comment
        fields = ['content']



class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        max_length=32,
        required=True,
        label='ユーザーネーム',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username']


class ProfileEditForm(forms.ModelForm):
    bio = forms.CharField(
        max_length=300,
        required=True,
        label='プロフィール',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )

    class Meta:
        model = Profile
        fields = ['bio']
