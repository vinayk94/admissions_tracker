from django import forms
from .models import AdmissionPost, Comment, User
from django.contrib.auth.forms import UserCreationForm

class AdmissionPostForm(forms.ModelForm):
    class Meta:
        model = AdmissionPost
        fields = ['degree_type', 'major', 'university', 'country', 'year', 'term', 'status', 'gpa', 'test_type', 'test_score', 'student_type', 'post_grad_plans', 'notes', 'notify_comments', 'email']
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 2000, 'max': 2100}),
            'term': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'notify_comments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notify_comments'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['notify_comments'].label = "Notify me of comments"
        self.fields['email'].required = False

    def clean(self):
        cleaned_data = super().clean()
        notify_comments = cleaned_data.get("notify_comments")
        email = cleaned_data.get("email")

        if notify_comments and not email:
            self.add_error('email', "Email is required when 'Notify me of comments' is checked.")

        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    anonymous_username = forms.CharField(max_length=30, required=False, help_text="Optional. This will be displayed instead of your username.")

    class Meta:
        model = User
        fields = ("username", "email", "anonymous_username", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username
    """
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different email.")
        return email
    """

    def clean_anonymous_username(self):
        anonymous_username = self.cleaned_data.get('anonymous_username')
        if anonymous_username and User.objects.filter(anonymous_username=anonymous_username).exists():
            raise forms.ValidationError("This anonymous username is already taken. Please choose a different one.")
        return anonymous_username
    
class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'anonymous_username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'anonymous_username': forms.TextInput(attrs={'class': 'form-control'}),
        }