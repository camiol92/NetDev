__author__ = 'Cami'

from django import forms
from django.http.request import QueryDict
from django.contrib.auth.models import User
from netdev.models import UserProfile, Topic, Post, Message, RepoFile, FileCategory

import datetime

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('display_name', 'picture', 'gender')

class UserFormExtra(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title', 'text')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'text', 'recipient', 'sender')

class RepoFileForm(forms.ModelForm):
#    eieiei = forms.CharField(label='Your name')

    class Meta:
        model = RepoFile
        #fields = ('name', 'description', 'stored_file', 'front', 'category', 'public')
        exclude = ('pub_date', 'last_mod', 'author',)

class FileCategoryForm(forms.ModelForm):

    class Meta:
        model = FileCategory
        exclude = ('owner',)

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('sender',)


# class TopicForm(forms.ModelForm):
#     title = forms.CharField(max_length=128, help_text="Por favor digite o Assunto do seu topico.")
#     text = forms.CharField(max_length=1024, help_text="Por favor digite o Conteudo do topico.")
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#     replies =  forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#     creation_date = forms.DateTimeField(widget=forms.HiddenInput, initial=datetime.datetime.now())
#     user = forms.CharField(max_length=1024, help_text='Selecione o usuario')
#
#
#     # An inline class to provide additional information on the form.
#     class Meta:
#         # Provide an association between the ModelForm and a model
#         model = Topic
#         fields = ('title', 'text', 'user')
#
# class PostForm(forms.ModelForm):
#     text = forms.CharField(max_length=128, help_text="Please enter the text")
#     user = forms.CharField(max_length=1024, help_text='Selecione o usuario')
#
#
#     class Meta:
#         # Provide an association between the ModelForm and a model
#         model = Post
#
#         # What fields do we want to include in our form?
#         # This way we don't need every field in the model present.
#         # Some fields may allow NULL values, so we may not want to include them...
#         # Here, we are hiding the foreign key.
#         fields = ('text', 'user')
# #
#
# class TopicCreateForm(forms.Form):
#     topic = forms.CharField(label="Topic", min_length=3)
#     message = forms.CharField(label="Message", min_length=3, widget=forms.Textarea())
#
# class PostCreateForm(forms.Form):
#     message = forms.CharField(label="Message", min_length=3, widget=forms.Textarea())