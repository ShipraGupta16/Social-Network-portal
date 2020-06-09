from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import *

def index(request):
    posts = Post.objects.order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "network/index.html", {"posts": posts})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# add post utility
@login_required
def add_post(request):
    content = request.POST.get('content')
    user = request.user
    post = Post(user=user, content=content)
    post.save()
    messages.success(request, "Successfully posted new tweet")
    return redirect("index")

# edit post utility
@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    content = request.POST.get('content')
    post.content = content
    post.save()
    # messages.success(request, "Successfully updated the tweet")
    return JsonResponse({"status": True})


# profile page utility with pagination enabled with minimum of 2 posts.
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    posts = user.posts.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "profile.html", {"user": user, "posts": posts})

# following utility.
@login_required
def following(request):
    user = User.objects.get(id=request.user.id)
    user_ids = Following.objects.filter(follower=user).values_list("user_id")
    posts = Post.objects.filter(user__in=user_ids)
    return render(request, "following.html", {"posts": posts})

# follow utility
@login_required
def follow(request, user_id):
    Following.objects.create(user_id=user_id, follower=request.user)
    messages.success(request, "Successfully followed the user")
    return redirect("profile", user_id=user_id)

# unfollow utility
@login_required
def unfollow(request, user_id):
    Following.objects.filter(user_id=user_id, follower=request.user).delete()
    messages.success(request, "Successfully unfollowed the user")
    return redirect("profile", user_id=user_id)

# like and unlike posts utility
def likeunlike(request, post_id):
    response = {
        "status": False,
        "message": "Please sign in to like"
    }
    if not request.user.is_authenticated:
        return JsonResponse(response)
    # unlike the post if user already liked and clicked on it again.
    if Like.objects.filter(user=request.user, post_id=post_id).exists():
        Like.objects.filter(user=request.user, post_id=post_id).delete()
        response['status'] = "unlike"
        response['message'] = "Successfully unliked the post"
        return JsonResponse(response)
    # like the post if user hasn't already liked it.
    Like.objects.create(user=request.user, post_id=post_id)
    response['status'] = "like"
    response['message'] = "Successfully liked the post"
    return JsonResponse(response)
