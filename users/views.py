from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserCreateForm
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
# Create your views here.

class LoginFormView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

def register(request):
    if request.method != "POST":
        form = UserCreateForm()
    else:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse("entries:main_page"))
    return render(request, "register.html", {"form": form})

def my_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("entries:main_page"))

def users(request):
    users = User.objects.filter(is_staff=False)
    return render(request, "users.html", {"users": users})

def add_user(request):
    form = UserCreateForm()
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse("users:users"))
    return render(request, "add_users.html", {"form": form})

def activate(request, username):
    user = User.objects.get(username=username)
    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse("users:users"))

def deactivate(request, username):
    user = User.objects.get(username=username)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse("users:users"))

def change_password(request, username):
    user = User.objects.get(username=username)
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse("users:users"))

    return render(request, "change_password.html", {"form": SetPasswordForm(user)})

def user_entries(request, username):
    user = User.objects.get(username=username)
