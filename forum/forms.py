from django import forms

from .models import Comment, Post


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
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '',
        }
