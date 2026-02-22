from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Message, Reply, Task

class MessageForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a message...'}),
        max_length=500,
        help_text="Maximum 500 characters."
    )

    class Meta:
        model = Message
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text.strip()) < 1:
            raise forms.ValidationError("Message cannot be empty.")
        return text

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text', 'emoji']

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        max_length=150,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text="Your password must contain at least 8 characters."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        help_text="Enter the same password as before, for verification."
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose a different username.')
        return username


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Görev başlığı...', 'class': 'form-control'}),
        max_length=200,
        label='Başlık'
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Görev açıklaması...', 'class': 'form-control'}),
        required=False,
        label='Açıklama'
    )
    status = forms.ChoiceField(
        choices=Task.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Durum'
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 1:
            raise forms.ValidationError("Başlık boş olamaz.")
        return title
