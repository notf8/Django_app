
from django.urls import path

from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    MyLoginView,
    AboutMeView,
    RegisterView,
    AboutMeUpdateView,
    ProfilesListView,
)


app_name = "myauth"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("", ProfilesListView.as_view(), name="profiles_list"),
    path("about-me/<int:pk>/", AboutMeView.as_view(), name="about-me"),
    path("about-me/<int:pk>/update/", AboutMeUpdateView.as_view(), name="profile_update"),
    path("cookie/get", get_cookie_view, name="cookie-get"),
    path("cookie/set", set_cookie_view, name="cookie-set"),
    path("session/get", get_session_view, name="session-get"),
    path("session/set", set_session_view, name="session-set"),
]
