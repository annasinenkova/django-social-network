from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import PostForm, CommentForm, ProfileForm, UserForm
from .models import Comments, Post, Profile


class PostCreate(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = PostForm()
            return render(request, 'tape/post_create.html', {'form': form})
        else:
            return redirect(reverse('login'))

    def post(self, request):
        bound_form = PostForm(request.POST, request.FILES)
        if bound_form.is_valid():
            bound_form = bound_form.save(commit=False)
            bound_form.user = request.user
            bound_form.save()
            return redirect(reverse('main'))
        return render(request, 'tape/post_create.html', {'form': bound_form})


def start(request):
    if request.user.is_authenticated:
        return redirect(reverse('main'))
    else:
        return redirect(reverse('login'))


@login_required
def main(request):
    posts = Post.objects.all().order_by('-created_date')
    profile = Profile.objects.get(user=request.user)
    return render(request, 'tape/tape.html', {'posts': posts, 'avatar': profile.avatar})


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user=request.user)
    return render(request, 'profile/profile.html', {'form': profile, 'posts': posts})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = UserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect(reverse('profile'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = UserForm(instance=request.user)
    return render(request, 'profile/edit_profile.html', {'profile_form': profile_form, 'user_form': user_form})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    profile = Profile.objects.get(user=request.user)
    comments = Comments.objects.filter(post=post).order_by('created_at')
    postAuthor = Profile.objects.get(user=post.user)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            post.comm += 1
            post.save()
            return redirect(request.path)
    else:
        comment_form = CommentForm()
    return render(request, 'tape/post_detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'avatar': profile.avatar, 'postAuthor': postAuthor})
