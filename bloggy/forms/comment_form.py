from bloggy.models.comment import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('use_name', 'user_email', 'comment_content')