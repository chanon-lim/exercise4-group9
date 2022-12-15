from django import forms
from .models import Post, Comment


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {'title': 'Title', 'content': 'Content'}

    # title = forms.CharField(label='Title', max_length=100)
    # content = forms.CharField(
    #     required=True,
    #     widget=forms.Textarea(
    #         attrs={
    #             'rows': 5,
    #             'placeholder': 'Content',
    #             }
    #         )
    #     )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
