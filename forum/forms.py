from django import forms
from .models import Post, Comment


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'tags',
        ]
        labels = {
            'title': 'Title',
            'content': 'Content',
            'tags': 'Tags',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs.update({'data-role': 'tagsinput'})

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
