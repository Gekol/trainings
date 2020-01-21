from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserCreateForm
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
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
            authenticated_user = authenticate(username=new_user.username, password=request.POST["password1"])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse("users:register"))
    return render(request, "register.html", {"form": form})

def my_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("entries:main_page"))