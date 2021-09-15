from django.urls import path
from .views import (
                    UserRegisterView,
                    LoginUser,
                    LogoutView,
                    HomePage,
                    CodeVerificationView,
                    ReestablecerPassView,
                    PanelUsuarioView
                    )

app_name='users_app'

urlpatterns = [
    path('registrar/',UserRegisterView.as_view(),name="registraruser"),
    path('login/',LoginUser.as_view(),name="loginuser"),      
    path('logout/',LogoutView.as_view(),name="logoutuser"), 
    path('panel/',HomePage.as_view(),name="paneluser"),
    path('user-verificacion/<int:pk>/',CodeVerificationView.as_view(),name="userverificacion"),
    path('reestablecerpass/',ReestablecerPassView.as_view(),name="reestablecerpass"),
    path('panel-usuario/',PanelUsuarioView.as_view(),name="panelusuario"),
    

]