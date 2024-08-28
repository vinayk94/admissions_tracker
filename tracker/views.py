from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from .models import AdmissionPost, Comment
from .forms import AdmissionPostForm, CommentForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('admission_dashboard')
        else:
            for error in form.error_messages:
                messages.error(request, form.error_messages[error])
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admission_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def admission_dashboard(request):
    sort_by = request.GET.get('sort', '-created_at')
    posts = AdmissionPost.objects.annotate(comment_count=Count('comments')).order_by(sort_by)
    
    if request.method == 'POST':
        form = AdmissionPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.user = request.user
            post.save()
            return redirect('admission_dashboard')
    else:
        form = AdmissionPostForm()
    
    context = {
        'posts': posts,
        'form': form,
        'comment_form': CommentForm(),
    }
    return render(request, 'tracker/admission_dashboard.html', context)

@require_POST
def like_post(request, post_id):
    post = get_object_or_404(AdmissionPost, id=post_id)
    if request.user.is_authenticated:
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
    else:
        liked = False
    
    return JsonResponse({
        'likes_count': post.likes.count(),
        'liked': liked,
        'authenticated': request.user.is_authenticated
    })

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(AdmissionPost, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'comment_content': comment.content,
            'comment_date': comment.created_at.strftime("%B %d, %Y %I:%M %p"),
            'comment_user': comment.user.username,
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)