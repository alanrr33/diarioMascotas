#from django.forms.forms import Form

from rest_framework.generics import ListAPIView
from django.contrib import messages
from django.views.generic import View,TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (UserRegisterForm,
                    LoginForm,
                    VerificationForm,
                    ReestablecerPassForm,
                    PanelUsuarioForm)
from .models import User
from .functions import generador_cod,generador_pass_temp
from .serializers import DueñoSerializer




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
            username=self.request.POST.get('username'),
            password=self.request.POST.get('password'),
            #username=form.cleaned_data['username'],
            #password=form.cleaned_data['password'],
        )


        if user is not None:
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

class ReestablecerPassView(FormView):
    template_name='users/reestablecerpass.html'
    form_class=ReestablecerPassForm
    success_url=reverse_lazy('users_app:loginuser')
    
    def form_valid(self,form):
        print('form valid')
        email=form.cleaned_data['email']
        messages.info(self.request, 'Se ha envíado un mail a su casilla con una contraseña temporal')
        contra=generador_pass_temp()

        #enviar pass al mail del usuario
        asunto='Contraseña temporal'
        mensaje='Esta es su contraseña temporal: ' + ' ' + contra
        email_remitente='alanrr33@gmail.com'
        
        send_mail(asunto,mensaje,email_remitente,[form.cleaned_data['email'],])

        #actualizamos la contraseña
        user=User.objects.get(
           email=email
        )
        user.set_password(contra)
        user.save()

        return super(ReestablecerPassView, self).form_valid(form)

class LogoutView(View):
    
    def get(self,request,*args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

class HomePage(LoginRequiredMixin,TemplateView):
    template_name="users/panel.html"
    login_url=reverse_lazy('users_app:loginuser')


class Index(TemplateView):
    template_name="users/index.html"

class PanelUsuarioView(LoginRequiredMixin,FormView):
    template_name='users/panel.html'
    form_class=PanelUsuarioForm
    success_url=reverse_lazy('users_app:loginuser')

    def form_valid(self, form):

        #actualizamos la contraseña
        user=self.request.user
        contra=form.cleaned_data['password1']
        user.set_password(contra)
        user.save()

        return super(PanelUsuarioView,self).form_valid(form)

class FaqView(LoginRequiredMixin,TemplateView):
    template_name="users/faq.html"




"APIS"

#Dueño
class BuscarDueñoApiView(ListAPIView):
    serializer_class=DueñoSerializer

    def get_queryset(self):
        kword=self.request.query_params.get('kword','')

        return User.objects.filter(
            nombre__icontains=kword
        ).order_by('nombre')



