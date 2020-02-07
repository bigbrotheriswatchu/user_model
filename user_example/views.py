from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.views.generic import RedirectView

from .forms import ExtendedUserCreationForm, UserProfileForm, PostForm
from .models import UserProfile, PostProfile
from django.contrib.auth.models import User
from django.core.paginator import Paginator

def index(request):
    posts = PostProfile.objects.filter().order_by('-created_at')
    paginator = Paginator(posts, 1)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    context = {'prev': prev_url, 'next': next_url, 'page_obj': page,}
    return render(request, 'user_example/index.html', context=context)


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


def post_detail(request, pk):
    post = get_object_or_404(PostProfile, pk=pk)
    return render(request, 'user_example/post_detail.html', context={'post': post})


def post_edit(request, pk):
    post = get_object_or_404(PostProfile, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            edit_post = form.save(commit=False)
            edit_post.user = request.user
            edit_post.updated_at = timezone.now()
            edit_post.save()
            return redirect('post_detail', pk=edit_post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'user_example/post_edit.html', context={'form': form})


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print(pk)

        obj = get_object_or_404(PostProfile, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user

        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_