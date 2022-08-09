from django.urls import path

import user_profile.views as view
from django.contrib.auth import views as au_views

urlpatterns = [
    path('login/', au_views.LoginView.as_view()),
    path('logout/', au_views.LogoutView.as_view()),
    path('register/', view.RegisterFormView.as_view()),
    path('profile/<int:user_id>/', view.profile),
    path('profile/<int:user_id>/questions/', view.profile),
    path('profile/<int:user_id>/answers/', view.profile),
    path('profile/<int:user_id>/edit/', view.edit_profile)
]