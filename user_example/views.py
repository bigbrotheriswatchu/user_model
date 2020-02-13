from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone

from .utils import ObjectDetailMixin
from django.views.generic import RedirectView,View

from .forms import ExtendedUserCreationForm, UserProfileForm, PostForm
from .models import UserProfile, PostProfile
from django.contrib.auth.models import User

from django.core.paginator import Paginator


def index(request):
    posts = PostProfile.objects.filter().order_by('-created_at')
    paginator = Paginator(posts, 3)

    users = User.objects.all()

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

    context = {'prev': prev_url, 'next': next_url, 'page_obj': page, "users": users}
    return render(request, 'user_example/index.html', context=context)


@login_required
def profile(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    posts = PostProfile.objects.filter().order_by('-created_at')

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
        form = UserProfileForm(request.POST, request.FILES or None, instance=profile_page)

        if form.is_valid():
            profile_user = form.save(commit=False)
            profile_user.user = request.user
            profile_user.save()
            return redirect('profile', pk=profile_user.pk)
    else:
        form = UserProfileForm(instance=profile_page)

    context = {'form': form}

    return render(request, 'user_example/edit_profile.html', context=context)


#class PostDelete(View):
    #def get(self, request, pk):
        #post = PostProfile.objects.get(pk=pk)
        #return render(request, 'user_example/post_delete_form.html', context={'post': post})

    #def post(self, request, pk):
        #profile_page = get_object_or_404(UserProfile, pk=pk)
        #post = PostProfile.objects.get(pk=pk)
       #post.delete()
        #return redirect('profile')


class PostDetail(ObjectDetailMixin, View):
    model = PostProfile
    template = 'user_example/post_detail.html'


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


def post_del(request, pk=None):
    post = get_object_or_404(PostProfile, pk=pk)
    post.delete()
    return redirect('profile', pk=request.user.userprofile.pk)


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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class PostLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(PostProfile, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user

        updated = False
        liked = False

        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)

            updated = True

        data = {
            "updated": updated,
            "liked": liked,
            }
        return Response(data)