from django import forms
from .models import AdmissionPost

class AdmissionPostForm(forms.ModelForm):
    class Meta:
        model = AdmissionPost
        fields = ['degree_type', 'major', 'university', 'country', 'application_round', 'status', 'gpa', 'test_type', 'test_score', 'student_type', 'post_grad_plans', 'notes']