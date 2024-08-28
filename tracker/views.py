from django.utils  import timezone
from django.shortcuts import render, redirect
from .models import AdmissionPost
from .forms import AdmissionPostForm
"""
def home(request):
    posts = AdmissionPost.objects.all()
    return render(request, 'tracker/home.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = AdmissionPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AdmissionPostForm()
    return render(request, 'tracker/create_post.html', {'form': form})

"""

def admission_dashboard(request):
    if request.method == 'POST':
        form = AdmissionPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.save()
            return redirect('admission_dashboard')
    else:
        form = AdmissionPostForm()
    
    posts = AdmissionPost.objects.all()
    universities = AdmissionPost.objects.values_list('university', flat=True).distinct()
    
    context = {
        'form': form,
        'posts': posts,
        'universities': universities,
        'degree_choices': AdmissionPost.DEGREE_CHOICES,
        'status_choices': AdmissionPost.STATUS_CHOICES,
    }
    return render(request, 'tracker/admission_dashboard.html', context)