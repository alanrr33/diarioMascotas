from django.urls import path
from .views import UserRegisterView,LoginUser,LogoutView,HomePage

app_name='users_app'

urlpatterns = [
    path('registrar/',UserRegisterView.as_view(),name="registraruser"),
    path('login/',LoginUser.as_view(),name="loginuser"),      
    path('logout/',LogoutView.as_view(),name="logoutuser"), 
    path('panel/',HomePage.as_view(),name="paneluser"),

]