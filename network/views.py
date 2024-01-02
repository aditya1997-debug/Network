from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json

from .models import User, Post
from .forms import Postform


def index(request):
    if request.method == 'POST':
        form = Postform(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.name = request.user
            form.save()
            return redirect(reverse('index'))
    else:
        p = Paginator(Post.objects.all(), 10)
        page = request.GET.get('page')
        all_posts = p.get_page(page)
        return render(request, 'network/index.html', {
            'post_form' : Postform(),
            'all_posts' : all_posts
        })

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

@login_required(login_url='login')
def profile(request, name):
    user_profile = User.objects.get(username=name)
    if request.user:
        in_list = User.objects.get(username = request.user)
    else:
        in_list = 'user'

    return render(request, "network/users.html", {
        "UserProfile" : user_profile.post_set.all().order_by('-date_posted'),
        "person" : user_profile,
        "following_list" : in_list
    })

def follow(request, person):
    x = User.objects.get(username=person)
    y = get_object_or_404(User, pk=x.id)
    user_list, created = User.objects.get_or_create(username=request.user)
    f = request.POST
    action = f.get("follow")
    if action == 'unfollow':
        user_list.following.remove(y)
    else:
        user_list.following.add(y)
    user_list.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def following(request):
    posts = []
    for i in request.user.following.all(): 
        for j in i.post_set.all():
            posts.append(j)

    p = Paginator(posts, 10)
    page = request.GET.get('page')
    followers_posts = p.get_page(page)

    return render(request, "network/following.html", {
        "posts" : followers_posts
    })

def edit(request, id):
   if request.method == 'POST':
        data = json.loads(request.body)
        edit_data = Post.objects.get(id=id)
        edit_data.post = data['post']
        edit_data.save()
        return JsonResponse({'data' : data['post']})

def like(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        if request.user not in post.liked_by.all():
            post.liked_by.add(request.user)
            post.save()
            return JsonResponse({'success' : True, 'liked' : True})
        else:
            post.liked_by.remove(request.user)
            post.save()
            return JsonResponse({'success' : True, 'liked': False})
    else:
        return JsonResponse({'success' : False})

def delete_post(request, id):
    if request.method == 'POST':
        #data = json.loads(request.body)
        post = get_object_or_404(Post, id=id)
        post.delete()
        return JsonResponse({'deleted' : True})
    else:
        return JsonResponse({'deleted' : False})