from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import UserEditView



#  hiiii

urlpatterns = [
    path('',views.logInPage,name='loginPage'),
    path('logout/',views.logOutPage,name="logout"),
    path('signup/',views.signUpPage,name='signUpPage'),
    path('home/',views.homePage,name='homePage'),
    # path('test/',views.test,name='test'),
    path('edit_profile/',UserEditView.as_view(),name='edit_profile'),
    path('password_reset/',views.forget_password,name='forget_password'),
]

# urlpatterns = [
#     path('',views.dashboard,name='dashboard'), 
#     path('login/',auth_views.LoginView.as_view(),name='login'),
#     path('logout/',auth_views.LogoutView)
# ]
