from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from django.views.generic import ListView
from .models import AdmissionPost, Comment, User
from .forms import AdmissionPostForm, CommentForm
from django.contrib import messages
import json
from .forms import UserSettingsForm
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str  
from django.utils.http import urlsafe_base64_decode





@login_required
def account_settings(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account settings have been updated.")
            return redirect('account_settings')
    else:
        form = UserSettingsForm(instance=request.user)
    return render(request, 'tracker/account_settings.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('home')
    return redirect('account_settings')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is verified
            user.generate_verification_token()
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('tracker/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user.verification_token,
            })
            user.email_user(subject, message)

            messages.success(request, 'Please confirm your email to complete registration.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and user.verification_token == token:
        user.is_active = True
        user.email_verified = True
        user.verification_token = ''
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('login')  
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('admission_timeline')  

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}! You have been logged in.")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': f"Welcome, {username}! You have been logged in."})
                else:
                    return redirect('admission_timeline')
            else:
                messages.error(request, "Invalid username or password.")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': "Invalid username or password."})
        else:
            messages.error(request, "Invalid username or password.")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': "Invalid username or password."})
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('admission_timeline')

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
            messages.success(request, "Your admission post has been created successfully.")
            return redirect('admission_timeline')
        else:
            print(form.errors)
            messages.error(request, "There was an error with your submission. Please check the form and try again.")
    else:
        form = AdmissionPostForm()
    
    sort_by = request.GET.get('sort', '-created_at')
    posts = AdmissionPost.objects.annotate(comment_count=Count('comments')).order_by(sort_by)
    
    context = {
        'posts': posts,
        'form': AdmissionPostForm(),
    }
    return render(request, 'tracker/admission_timeline.html', context)

class AdmissionStatsView(ListView):
    model = AdmissionPost
    template_name = 'tracker/admission_stats.html'
    context_object_name = 'admissions'

    STATUS_GROUPS = {
        'admissions': ['ACCEPTED', 'ACCEPTED FROM WAITLIST', 'ENROLLED'],
        'rejections': ['REJECTED', 'REJECTED FROM WAITLIST'],
        'in_progress': ['APPLIED', 'APPLYING', 'WAITLISTED', 'INTERVIEW'],
        'questions': ['QUESTION'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter based on query parameters
        filters = {}
        if self.request.GET.get('university'):
            filters['university__icontains'] = self.request.GET['university']
        if self.request.GET.get('major'):
            filters['major__icontains'] = self.request.GET['major']
        if self.request.GET.get('degree_type'):
            filters['degree_type'] = self.request.GET['degree_type']
        if self.request.GET.get('year'):
            filters['year'] = self.request.GET['year']
        if self.request.GET.get('term'):
            filters['term'] = self.request.GET['term']

        queryset = queryset.filter(**filters)

        count_type = self.request.GET.get('count_type', 'all')
        if count_type != 'all' and count_type in self.STATUS_GROUPS:
            queryset = queryset.filter(status__in=self.STATUS_GROUPS[count_type])

        return queryset.values('university', 'major', 'degree_type', 'year', 'term').annotate(
            admissions_count=Count('id', filter=Q(status__in=self.STATUS_GROUPS['admissions'])),
            rejections_count=Count('id', filter=Q(status__in=self.STATUS_GROUPS['rejections'])),
            in_progress_count=Count('id', filter=Q(status__in=self.STATUS_GROUPS['in_progress'])),
            questions_count=Count('id', filter=Q(status__in=self.STATUS_GROUPS['questions'])),
            total_count=Count('id')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['universities'] = AdmissionPost.objects.values_list('university', flat=True).distinct()
        context['majors'] = AdmissionPost.objects.values_list('major', flat=True).distinct()
        context['degree_types'] = dict(AdmissionPost.DEGREE_CHOICES)
        context['years'] = AdmissionPost.objects.values_list('year', flat=True).distinct().order_by('-year')
        context['terms'] = dict(AdmissionPost.TERM_CHOICES)
        context['count_types'] = [
            ('all', 'All Statuses'),
            ('admissions', 'Admissions'),
            ('rejections', 'Rejections'),
            ('in_progress', 'In Progress'),
            ('questions', 'Questions'),
        ]
        return context

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(AdmissionPost, id=post_id)
    data = json.loads(request.body)
    form = CommentForm(data)
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
            'comment_user': comment.user.get_display_name(),
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@require_POST
def like_post(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'You must be logged in to like a post.'}, status=403)
    
    post = get_object_or_404(AdmissionPost, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'success': True,
        'likes_count': post.likes.count(),
        'liked': liked,
    })


@login_required
@require_POST
def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    data = json.loads(request.body)
    content = data.get('content')
    if content:
        reply = Comment.objects.create(
            post=parent_comment.post,
            user=request.user,
            content=content,
            parent=parent_comment
        )
        return JsonResponse({
            'success': True,
            'reply_id': reply.id,
            'reply_content': reply.content,
            'reply_date': reply.created_at.strftime("%B %d, %Y %I:%M %p"),
            'reply_user': reply.user.username,
        })
    return JsonResponse({'success': False, 'error': 'Reply content is required.'}, status=400)

def get_comments(request, post_id):
    post = get_object_or_404(AdmissionPost, id=post_id)
    comments = post.comments.all().order_by('created_at')
    comment_data = [{
        'id': comment.id,
        'user': comment.user.username,
        'content': comment.content,
        'created_at': comment.created_at.strftime("%B %d, %Y %I:%M %p"),
        'replies': [{
            'id': reply.id,
            'user': reply.user.username,
            'content': reply.content,
            'created_at': reply.created_at.strftime("%B %d, %Y %I:%M %p"),
        } for reply in comment.replies.all()]
    } for comment in comments]
    return JsonResponse({'comments': comment_data})

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        post_id = comment.post.id
        comment.delete()
        return JsonResponse({'success': True, 'post_id': post_id})
    return JsonResponse({'success': False, 'error': 'You are not authorized to delete this comment.'}, status=403)