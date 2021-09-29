#-*-coding: utf8-*-
from django import forms
from .models import Comment

class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, label="Оставить коментарий")

    def save(self, blog=None, user=None, ip=None):
        if self.cleaned_data['body'] and blog and user:
            comment = Comment(body=self.cleaned_data['body'], blog=blog,
                                                              user=user)
            if ip:
                comment.ip = ip
            comment.save()
