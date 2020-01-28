from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.utils import timezone

from .forms import ExtendedUserCreationForm, UserProfileForm, PostForm
from .models import UserProfile, PostProfile
from django.contrib.auth.models import User


def index(request):
    posts = PostProfile.objects.filter().order_by('-created_at')

    return render(request, 'user_example/index.html', context={'posts': posts,
                                                               })


@login_required
def profile(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)

    user = get_object_or_404(User, pk=pk)
    posts = PostProfile.objects.filter(author=user)

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_form = post_form.save(commit=False)
            post_form.author = request.user
            post_form.created_at = timezone.now()
            post_form.save()
            return redirect('profile', pk=profile.pk)
    else:
        post_form = PostForm()
    return render(request, 'user_example/profile.html', context={'posts': posts,
                                                                 'profile': profile,
                                                                 'form': post_form,
                                                                 })


def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():

            user = form.save()
            person = profile_form.save(commit=False)
            person.user = user
            person.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('profile', pk=person.pk)
    else:
        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/register.html', context={'form': form,
                                                                  'profile_form': profile_form
                                                                  })


def profile_edit(request, pk):
    profile_page = get_object_or_404(UserProfile, pk=pk)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile_page)

        if form.is_valid():
            profile_user = form.save(commit=False)
            profile_user.user = request.user
            profile_user.save()
            return redirect('profile', pk=profile_user.pk)
    else:
        form = UserProfileForm(instance=profile_page)

    context = {'form': form}

    return render(request, 'user_example/edit_profile.html', context=context)


