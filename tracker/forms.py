from django import forms
from .models import AdmissionPost, Comment
from django.contrib.auth.forms import UserCreationForm
from .models import User

class AdmissionPostForm(forms.ModelForm):
    class Meta:
        model = AdmissionPost
        fields = ['degree_type', 'major', 'university', 'country', 'application_round', 'status', 'gpa', 'test_type', 'test_score', 'student_type', 'post_grad_plans', 'notes', 'email', 'notify_comments']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'notify_comments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),

        }

class CustomUserCreationForm(UserCreationForm):
    anonymous_username = forms.CharField(max_length=30, required=False, help_text="Optional. This will be displayed instead of your username.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('anonymous_username',)