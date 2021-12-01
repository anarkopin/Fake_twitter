from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control w-100',
                                                            'id': 'contentsBox',
                                                            'rows': '3',
                                                            'placeholder':'¿Que esta pasando?'}))  #esta variable tomara el lugar del text area que elminaremos

    class Meta:
        model = Post
        fields = {'content'} 


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User   #modelo que queremos usar
        fields = ['first_name', 'username']   #campos del modelo que queremos editar
         
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','bio']