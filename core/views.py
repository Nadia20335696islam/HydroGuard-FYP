from django.shortcuts import render, redirect
from accounts.models import User

def dashboard(request):
    user_id = request.session.get("user_id")
    is_guest = request.session.get("guest") is True

    if not user_id and not is_guest:
        return redirect("accounts:login")


    user = None
    if user_id:
        user = User.objects.get(id=user_id)

    return render(request, "core/dashboard.html", {"user": user, "is_guest": is_guest})
def home(request):
    return render(request, "core/home.html")