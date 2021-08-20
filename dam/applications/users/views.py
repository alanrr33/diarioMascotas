#from django.forms.forms import Form
from django.contrib import messages
from django.views.generic import View,TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from .forms import (UserRegisterForm,
                    LoginForm,
                    VerificationForm,)
from .models import User
from .functions import generador_cod




# Create your views here.


class UserRegisterView(FormView):
    template_name='users/registrar.html'
    form_class=UserRegisterForm
    #success_url=reverse_lazy('index')

    def form_valid(self, form):
        #generar codigo aleatorio
        codigo=generador_cod()

        print(form.cleaned_data['nombre'])
        print(form.cleaned_data['apellido'])
        usuario=User.objects.create_user(
            
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombre=form.cleaned_data['nombre'],
            apellido=form.cleaned_data['apellido'],
            genero=form.cleaned_data['genero'],
            cod_registro=codigo,
            
        )
        #enviar codigo al mail del usuario
        asunto='Confirmación de email'
        mensaje='Codigo de verificación' + ' ' + codigo
        email_remitente='alanrr33@gmail.com'
        #
        send_mail(asunto,mensaje,email_remitente,[form.cleaned_data['email'],])
        #redirigir a pantalla de validación

        return HttpResponseRedirect(
            reverse(
                'users_app:userverificacion',
                kwargs={'pk': usuario.id}
            )
        )


        #return super(UserRegisterView,self).form_valid(form)

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

class CodeVerificationView(FormView):

    template_name='users/verification.html'
    form_class=VerificationForm
    success_url=reverse_lazy('users_app:loginuser')

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self,form):

        User.objects.filter(
           id=self.kwargs['pk']
        ).update(
           is_active=True
        )

        messages.success(self.request, 'Verificación exitosa !')


        return super(CodeVerificationView, self).form_valid(form)



class LogoutView(View):
    
    def get(self,request,*args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

class HomePage(LoginRequiredMixin,TemplateView):
    template_name="users/panel.html"
    login_url=reverse_lazy('users_app:loginuser')


class Index(TemplateView):
    template_name="users/index.html"





