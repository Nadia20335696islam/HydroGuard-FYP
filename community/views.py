"""
Views for the Community app.

This module contains the main request handlers for the
HydroGuard community feature.

Supported functionality:
- display the community feed
- create new community posts
- display individual post details
- add comments to posts
- like and unlike posts

Guest support:
- guest users may view the main community feed in read-only mode
- interactive community actions remain restricted to registered users
"""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from .forms import CommunityPostForm, CommentForm
from .models import CommunityPost, Comment, PostLike


# ==================================================
# HELPER FUNCTION: GET CURRENT AUTHENTICATED USER
# ==================================================
def get_logged_in_user(request):
    """
    Returns the currently logged-in custom user based on
    the session value stored by the accounts app.

    Returns:
        User object if a valid session exists
        None if no authenticated user is found
    """
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


# ==================================================
# HELPER FUNCTION: CHECK GUEST SESSION
# ==================================================
def is_guest_user(request):
    """
    Returns True if the current session belongs to a guest user.

    This is used to allow limited read-only access to selected
    parts of the HydroGuard platform without requiring registration.
    """
    return request.session.get("guest") is True


# ==================================================
# COMMUNITY FEED VIEW
# ==================================================
def community_feed(request):
    """
    Displays the main community feed.

    This page shows all community posts in reverse
    chronological order so that the newest posts appear first.

    Access control:
    - authenticated users may access the feed normally
    - guest users may access the feed in read-only mode
    - users with neither session type are redirected to login
    """
    user = get_logged_in_user(request)
    is_guest = is_guest_user(request)

    # Allow access for logged-in users and guest users only
    if not user and not is_guest:
        messages.error(request, "Please log in to access the community space.")
        return redirect("accounts:login")

    posts = CommunityPost.objects.select_related("author").prefetch_related(
        "comments",
        "likes"
    ).order_by("-created_at")

    context = {
        "user": user,
        "posts": posts,
        "is_guest": is_guest,
    }
    return render(request, "community/community_feed.html", context)


# ==================================================
# CREATE COMMUNITY POST VIEW
# ==================================================
def create_post(request):
    """
    Handles creation of a new community post.

    Users can create either:
    - a water-saving tip
    - a local water issue report

    GET:
        Displays an empty post creation form

    POST:
        Validates and saves the form if valid

    Access control:
    - only authenticated registered users may create posts
    - guest users are redirected back to the feed
    """
    user = get_logged_in_user(request)

    if not user:
        if is_guest_user(request):
            messages.error(request, "Guest users can view tips, but must register to create posts.")
            return redirect("community:community_feed")

        messages.error(request, "Please log in to create a community post.")
        return redirect("accounts:login")

    if request.method == "POST":
        form = CommunityPostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()

            messages.success(request, "Your community post has been published successfully.")
            return redirect("community:community_feed")
    else:
        form = CommunityPostForm()

    context = {
        "form": form,
        "user": user,
    }
    return render(request, "community/create_post.html", context)


# ==================================================
# COMMUNITY POST DETAIL VIEW
# ==================================================
def post_detail(request, post_id):
    """
    Displays the full details of a single community post.

    This page shows:
    - the selected post
    - all comments related to the post
    - a comment submission form
    - current like state for the logged-in user

    Access control:
    - only authenticated registered users may open the full
      interactive post detail page
    """
    user = get_logged_in_user(request)

    if not user:
        if is_guest_user(request):
            messages.error(request, "Guest users can view the community feed, but must register to open full post details.")
            return redirect("community:community_feed")

        messages.error(request, "Please log in to view community posts.")
        return redirect("accounts:login")

    post = get_object_or_404(
        CommunityPost.objects.select_related("author").prefetch_related("comments__author", "likes"),
        id=post_id
    )

    comments = post.comments.select_related("author").order_by("created_at")
    comment_form = CommentForm()

    user_has_liked = PostLike.objects.filter(post=post, user=user).exists()

    context = {
        "user": user,
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
        "user_has_liked": user_has_liked,
    }
    return render(request, "community/post_detail.html", context)


# ==================================================
# ADD COMMENT VIEW
# ==================================================
def add_comment(request, post_id):
    """
    Handles submission of a new comment for a specific post.

    POST only:
    - validates submitted comment form
    - attaches the logged-in user as the comment author
    - links the comment to the target post

    Access control:
    - only authenticated registered users may comment
    """
    user = get_logged_in_user(request)

    if not user:
        if is_guest_user(request):
            messages.error(request, "Guest users can view tips, but must register to comment.")
            return redirect("community:community_feed")

        messages.error(request, "Please log in to comment on a post.")
        return redirect("accounts:login")

    post = get_object_or_404(CommunityPost, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = user
            comment.post = post
            comment.save()

            messages.success(request, "Your comment has been added successfully.")
        else:
            messages.error(request, "Unable to add comment. Please check your input.")

    return redirect("community:post_detail", post_id=post.id)


# ==================================================
# TOGGLE LIKE VIEW
# ==================================================
def toggle_like(request, post_id):
    """
    Adds or removes a like for the selected post.

    Behaviour:
    - if the user has not liked the post, a like is created
    - if the user has already liked the post, the like is removed

    This creates a simple toggle-like mechanism for community
    interaction.

    Access control:
    - only authenticated registered users may like posts
    """
    user = get_logged_in_user(request)

    if not user:
        if is_guest_user(request):
            messages.error(request, "Guest users can view tips, but must register to like posts.")
            return redirect("community:community_feed")

        messages.error(request, "Please log in to like community posts.")
        return redirect("accounts:login")

    post = get_object_or_404(CommunityPost, id=post_id)

    existing_like = PostLike.objects.filter(post=post, user=user).first()

    if existing_like:
        existing_like.delete()
        messages.success(request, "You removed your like from this post.")
    else:
        PostLike.objects.create(post=post, user=user)
        messages.success(request, "You liked this post.")

    return redirect("community:post_detail", post_id=post.id)