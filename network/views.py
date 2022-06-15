from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *


def index(request):
    posts = Post.objects.all().order_by('-time')
    # Set the paginator to 10 pages:
    paginator = Paginator(posts, 10)
    # Get the page number of the URL, if nothing exists come back to page 1:
    pageNumber = request.GET.get('page')
    page_obj = paginator.get_page(pageNumber)
    # List of all profiles ordered randomly:
    allProfiles = Profile.objects.all().order_by('?')
    if request.user.is_authenticated:
        # Let users publish posts:
        postForm = PostForm(request.POST)
        if request.method == 'POST':
            prof_id = Profile.objects.get(user=request.user)
            if postForm.is_valid():
                post = postForm.save(commit=False)
                post.user = request.user
                post.save()
                post.profile = prof_id
                post.save()
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, "network/index.html", {
                    "allProfiles": allProfiles,
                    "postForm": postForm,
                    "posts": posts,
                    "page_obj": page_obj
                })
    # Not logged users just can view all posts and other user's profiles:
    else:
        return render(request, "network/index.html", {
            "allProfiles": allProfiles,
            "posts": posts,
            "page_obj": page_obj
        })
    return render(request, "network/index.html", {
        "allProfiles": allProfiles,
        "postForm": postForm,
        "posts": posts,
        "page_obj": page_obj,
        "profile": Profile.objects.get(user=request.user),
        "following": Profile.objects.get(user=request.user).following.all(),
        "userFollow": Profile.objects.get(user=request.user).following
    })


@login_required
def bio(request):
    user = request.user
    profileForm = ProfileForm(request.POST)
    if request.method == 'POST':
        if profileForm.is_valid():
            profile = profileForm.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect(reverse("index"))
    return render(request, "network/bio.html", {
        "profileForm": profileForm,
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        profile = Profile.objects.filter(user__id=request.user.id)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            if profile:
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/index.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/index.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            # Using keyword argument, I finally avoid problems with create_user including more than 4 arguments.
            user = User.objects.create_user(
                username=username, email=email, password=password, last_name=last_name, first_name=first_name)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("bio"))
    else:
        return render(request, "network/register.html")


# Function to load the profile of the user, including his/her posts
# (using paginator) and follow/unfollow button:
def profile(request, username):
    follow = request.user
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by('-time')
    profiler = Profile.objects.get(user=user)
    profile = Profile.objects.get(user=request.user)
    pageNumber = request.GET.get('page')
    paginator = Paginator(posts, 16)
    page_obj = paginator.get_page(pageNumber)
    # Follow/unfollow actions via post method.
    # If follow is clicked, add that user to the following list:
    if request.method == 'POST' and request.POST.get('Follow'):
        profiler.follower.add(follow)
        profiler.save()
        profile.following.add(user)
        profile.save()
        # After click the button, redirect to user's profile (comma is necessary
        # in args because it is inside a tuple with only 1 element):
        return HttpResponseRedirect(reverse('profile', args=(username,)))
    # If click unfollow, remove that user from the followig list:
    if request.method == 'POST' and request.POST.get('Unfollow'):
        profiler.follower.remove(follow)
        profiler.save()
        profile.following.remove(user)
        profile.save()
        return HttpResponseRedirect(reverse('profile', args=(username,)))
    # Finally, pass the variables as context:
    return render(request, "network/profile.html", {
        'profiler': profiler,
        'profile': profile,
        'posts': posts,
        'user': user,
        'page_obj': page_obj
    })


@login_required
# Create the list 'following' and order posts by timestamp:
# Logged users can add or remove other users from his/her following list:
def follow_user(request):
    following = Profile.objects.get(user=request.user).following.all()
    userFollow = Profile.objects.filter(user__in=following)
    posts = Post.objects.filter(user__in=following).order_by('-time')
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get('page')
    page_obj = paginator.get_page(pageNumber)
    return render(request, "network/following.html", {
        'profile': Profile.objects.get(user=request.user),
        'allProfiles': Profile.objects.all().order_by('?'),
        'posts': posts,
        'page_obj': page_obj,
        'following': following,
        'userFollow': userFollow
    })


@csrf_exempt
@login_required
# Get the call via JS to add or remove Likes from the likelist:
def like(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        try:
            # If logged user didn't click Like before, add her/him:
            post = Post.objects.get(id=post_id)
            if request.user in post.like.all():
                post.like.remove(request.user)
                post.save()
                count = post.like.count()
                return JsonResponse({
                    'count': count,
                    "status":201
                })
            # If logged user clicked Like already, remove her/him:
            else:
                post.like.add(request.user)
                post.save()
                count = post.like.count()
                return JsonResponse({'count': count, "status":201})
        except:
            return JsonResponse({}, status=404)
    return JsonResponse({}, status=404)



@login_required
def unlike(request, post_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(username=request.user)
    post.like.remove(user)
    post.save
    return HttpResponseRedirect(reverse("index"))



@csrf_exempt
@login_required
def delete_post(request):
    if request.method == "POST":
        try:
            post_id = request.POST.get('id')
            post = Post.objects.get(id=post_id)
            post.delete()
            return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)
    return JsonResponse({}, status=400)



@csrf_exempt
@login_required
def edit_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('id')
        post_body = request.POST.get('post')
        
        print(post_body)
        try:
            post = Post.objects.get(id=post_id)
            post.comment = post_body
            post.save()
            print('prueba')
            return JsonResponse({}, status=201)
        except:
            print('pruebax')
            return JsonResponse({}, status=404)
    return JsonResponse({}, status=400)

