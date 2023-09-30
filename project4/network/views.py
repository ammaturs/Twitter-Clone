from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django import forms
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .net_helper import unfollowed, followed
from django.core.paginator import Paginator
import json

from .models import User, Posts, Profile

class NewPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Whats on your mind?', 'style': 'width: calc(100% - 10px); height:100px;', 'class': 'form-control'}))


def index(request):
    #new post created
    if request.method == "POST":
        form=NewPostForm(request.POST)
        if form.is_valid():
            content =form.cleaned_data['content']

            posting = Posts(
                    user=request.user,
                    content = content,
                    created = datetime.now()
                )
            posting.save()
            return redirect('index')
        else:
            return render(request, "network/index.html", {"form":form})
    else:
        #show all posts
        posts = Posts.objects.all().order_by('-created')

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        return render(request, "network/index.html", {"form":NewPostForm(), "page":page})


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
            profile = Profile(user=user)
            user.save()
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, user):
    user_obj = User.objects.get(username=user) #get the user whos profile were on
    user_profile = Profile.objects.get(user=user_obj) #get the users whos profile were on profile, can access followers from here
    logged_in_user = request.user

    if request.method == "POST":
        #user either request to follow or unfollow
        #logged in user visits a profile they currently follower and send a post request meaning they unfollowed request
        #logged in users following goes down 1, profile users followers go down 1
        if logged_in_user in user_profile.followers.all():
            unfollowed(logged_in_user, user)
            follows=False

        else:
            followed(logged_in_user, user)
            follows=True

        posts = Posts.objects.filter(user = user_obj).order_by('-created') #get specific users posts

        paginator = Paginator(posts, 10)  # Change 10 to the desired number of items per page
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        follower_count = user_profile.followers.all().count()
        following_count = user_profile.following.all().count()
        return render(request, "network/profile.html", {"follows":follows,"user":user_obj,"page":page, "follower_count":follower_count, "following_count":following_count})

    else:

        #a different person requested to view a profile, we need to know if the logged in person follows that person already
        if request.user != user:
            if logged_in_user in user_profile.followers.all():
                follows=True
            else:
                follows=False

        posts = Posts.objects.filter(user = user_obj).order_by('-created') #get specific users posts

        paginator = Paginator(posts, 10)  # Change 10 to the desired number of items per page
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)



        follower_count = user_profile.followers.all().count()
        following_count = user_profile.following.all().count()
        return render(request, "network/profile.html", {"follows":follows,"user":user_obj,"page":page, "follower_count":follower_count, "following_count":following_count})

@login_required
def following(request):

    #get the profile of the user whos logged in
    user_obj = User.objects.get(username=request.user)

    #get the user profile
    user_profile = Profile.objects.get(user=user_obj)

    #who the user follows
    user_following = user_profile.following.all()

    following_feed = []
    #for every person the user follows, get all their posts
    for entry in user_following:
        follower_posts = Posts.objects.filter(user=entry)
        for item in follower_posts: #if user has more than one post, need to loop through each post from that single user
            following_feed.append({"user":item.user, "content":item.content,"created":item.created, "likes":item.likes, "id":item.id})


    following_feed = sorted(following_feed, key=lambda x: x["created"], reverse=True)

    paginator = Paginator(following_feed, 10)  # Change 10 to the desired number of items per page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "network/following.html", {"page":page})


#this will be our endpoint where we save our content edits to our database
def edit(request, postId):
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))

        #we got the new content and a postId, now save to that post id in posts the new cotnent
        post = Posts.objects.get(id=postId)
        post.content = data['new_content']
        post.save()
        return JsonResponse({'message': 'Edit successful'})

def like(request, postId):
    if request.method=="POST":

        #we got a new like, add 1 to like count on post
        post = Posts.objects.get(id=postId)
        post.likes +=1
        post.save()
        return JsonResponse({'likes': post.likes})



