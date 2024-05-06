from django.urls import include, re_path
from UserApp import views as UserAppViews

urlpatterns = [
    re_path(r"^register/$", UserAppViews.Signup.as_view()),
    re_path(r"^login/$", UserAppViews.UserLogin.as_view()),
    re_path(r"^setpassword/$", UserAppViews.SetPassword.as_view()),
    re_path(r"^imageupload/$", UserAppViews.FileUpload.as_view()),
    re_path(r"^get_customer/(?P<pk>[0-9]+)/$", UserAppViews.GetCustomer.as_view()),
]
