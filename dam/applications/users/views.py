from django.views.generic import View,TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm,LoginForm
from .models import User




# Create your views here.

class UserRegisterView(FormView):
    template_name='users/registrar.html'
    form_class=UserRegisterForm
    success_url=reverse_lazy('index')

    def form_valid(self, form):
        print(form.cleaned_data['nombre'])
        print(form.cleaned_data['apellido'])
        User.objects.create_user(
            
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombre=form.cleaned_data['nombre'],
            apellido=form.cleaned_data['apellido'],
            genero=form.cleaned_data['genero'],
            
        )

        return super(UserRegisterView,self).form_valid(form)

class LoginUser(FormView):
    template_name='users/login.html'
    form_class=LoginForm
    success_url=reverse_lazy('mascotas_urls:listarmascotas' )

    def form_valid(self,form):

        user=authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        login(self.request,user)

        return super(LoginUser, self).form_valid(form)

class LogoutView(View):
    
    def get(self,request,*args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

class HomePage(LoginRequiredMixin,TemplateView):
    template_name="users/panel.html"
    login_url=reverse_lazy('users_app:loginuser')


class Index(TemplateView):
    template_name="users/index.html"





