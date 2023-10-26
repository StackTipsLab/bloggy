from django import forms

from bloggy.models.comment import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('use_name', 'user_email', 'comment_content')

