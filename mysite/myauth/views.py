import copy
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from .models import Profile
from .forms import ProfileForm, UserForm


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response


class AboutMeView(DetailView):
    template_name = "myauth/about-me.html"
    queryset = User.objects.all()


class MyLoginView(LoginView):
    template_name = 'myauth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse(
                "myauth:about-me",
                kwargs={'pk': self.request.user.id},
            )


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


class AboutMeUpdateView(UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name_suffix = "_update_form"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.id == self.get_object().user.id

    def get_success_url(self):
        return reverse(
            "myauth:about-me",
            kwargs={'pk': self.get_object().user.id},
        )


class ProfilesListView(ListView):
    template_name = 'myauth/profiles-list.html'
    context_object_name = "users"
    queryset = User.objects.prefetch_related()


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")



