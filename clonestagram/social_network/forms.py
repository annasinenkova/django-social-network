from django import forms
from .models import Post, Profile, Comments
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption', 'photo')
        widgets = {
            'caption': forms.TextInput(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={"class": "form-control", "id": "comment", "required": "True", }),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('country', 'bio', 'birth_date', 'avatar')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
