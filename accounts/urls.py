from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from .views import UserEditView



#  hiiii

urlpatterns = [
    path('',views.logInPage,name='loginPage'),
    path('logout/',views.logOutPage,name="logout"),
    path('signup/',views.signUpPage,name='signUpPage'),
    path('home/',views.homePage,name='homePage'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
    path('resetPassword_validate/<uidb64>/<token>/',views.resetPassword_validate,name='resetPassword_validate'),
    path('resetPassword/',views.resetPassword,name='resetPassword'),
    # path('test/',views.test,name='test'),
    # path('edit_profile/',UserEditView.as_view(),name='edit_profile'),
    # path('password_reset/',views.forget_password,name='forget_password'),
    # path('<id>/password/',auth_views.PasswordChangeView.as_view(template_name='userside/change_password.html')),
]

# urlpatterns = [
#     path('',views.dashboard,name='dashboard'), 
#     path('login/',auth_views.LoginView.as_view(),name='login'),
#     path('logout/',auth_views.LogoutView)
# ]
