from django.shortcuts import render, redirect
from .models import AdmissionPost
from .forms import AdmissionPostForm

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