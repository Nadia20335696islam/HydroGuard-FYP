from django.shortcuts import render, redirect
from django.db import IntegrityError

from .models import User
from .security import hash_password
from .validators import is_valid_email, password_issues
from .security import verify_password
from .validators import is_valid_email

def register(request):
    if request.method == "GET":
        return render(request, "accounts/register.html")

    first_name = (request.POST.get("first_name") or "").strip()
    last_name = (request.POST.get("last_name") or "").strip()
    email = (request.POST.get("email") or "").strip().lower()
    password = request.POST.get("password") or ""
    confirm = request.POST.get("confirm") or ""

    errors = []

    if not first_name:
        errors.append("First name is required.")
    if not last_name:
        errors.append("Last name is required.")

    if not email or not is_valid_email(email):
        errors.append("Please enter a valid email address.")

    pwd_errors = password_issues(password)
    if pwd_errors:
        errors.extend(pwd_errors)

    if password != confirm:
        errors.append("Passwords do not match.")

    if errors:
        return render(request, "accounts/register.html", {"errors": errors, "data": request.POST})

    try:
        password_hash, salt = hash_password(password)
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash,
            salt=salt,
        )

        # ✅ Auto-login after register
        request.session["user_id"] = user.id
        request.session["guest"] = False

        # ✅ Go to dashboard
        return redirect("/dashboard/")

    except IntegrityError:
        return render(request, "accounts/register.html", {
            "errors": ["An account with this email already exists."],
            "data": request.POST
        })
 
def guest_login(request):
    request.session.flush()
    request.session["guest"] = True
    request.session["user_id"] = None
    return redirect("/dashboard/") 

def login_view(request):
    # If already logged in, go dashboard
    if request.session.get("user_id"):
        return redirect("/dashboard/")

    if request.method == "GET":
        return render(request, "accounts/login.html")

    # POST
    email = (request.POST.get("email") or "").strip().lower()
    password = request.POST.get("password") or ""

    errors = []

    if not email or not is_valid_email(email):
        errors.append("Please enter a valid email address.")
    if not password:
        errors.append("Password is required.")

    if not errors:
        user = User.objects.filter(email=email).first()
        if not user:
            errors.append("No account found with that email.")
        else:
            if verify_password(password, user.salt, user.password_hash):
                request.session["user_id"] = user.id
                request.session["guest"] = False
                return redirect("/dashboard/")
            errors.append("Incorrect password.")

    return render(request, "accounts/login.html", {"errors": errors, "email": email})


def logout_view(request):
    request.session.flush()
    return redirect("/accounts/login/")


def forgot_password(request):
    # For now: a safe placeholder page (no email sending yet)
    # Later you can implement token reset flow.
    if request.method == "GET":
        return render(request, "accounts/forgot_password.html")

    email = (request.POST.get("email") or "").strip().lower()
    message = "If an account exists for that email, we’ll send reset instructions."

    # We do NOT confirm whether the email exists (security best practice)
    return render(request, "accounts/forgot_password.html", {"message": message, "email": email}) 

