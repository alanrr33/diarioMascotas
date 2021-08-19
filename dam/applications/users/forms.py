from django import forms
from django.contrib.auth import authenticate
from .models import User

class UserRegisterForm(forms.ModelForm):

    password1=forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder':'Contraseña'
        }
    ))

    password2=forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder':'Repetir Contraseña'
        }
    ))

    class Meta:
        model=User
        fields=(
            'username',
            'email',
            'nombre',
            'apellido',
            'genero',

        )

    #al hacer validacion de varios campos debemos sobreescribir el metodo clean
    def clean(self):
        cleaned_data=super(UserRegisterForm, self).clean()

        password1=self.cleaned_data['password1']
        password2=self.cleaned_data['password2']
        
        if password1 and password2:
            if password1 != password2:
                self.add_error('password2','Las contraseñas no coinciden')

        if (len(password1)<5):
            self.add_error('password1','La contraseña debe tener más de 5 caracteres')
        
        if (len(password2)<5):
            self.add_error('password2','La contraseña debe tener más de 5 caracteres')
        

        username=self.cleaned_data['username']
        nombre=self.cleaned_data['nombre']
        #print(username)
        #print(nombre)

        if username and nombre:
            if username==nombre:
                self.add_error('nombre','El nombre no puede ser el mismo que username')


        return cleaned_data
    

class LoginForm(forms.Form):

    username=forms.CharField(label='Usuario', required=True, widget=forms.TextInput(
        attrs={
            'placeholder':'Usuario',
            'style': '{ margin:10px }',
        }
    ))

    password=forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder':'Contraseña'
        }
    ))
    
    def clean(self):
        cleaned_data=super(LoginForm, self).clean()
        username=self.cleaned_data['username']
        password=self.cleaned_data['password']

        if not authenticate(username=username,password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')
        return cleaned_data
    
class VerificationForm(forms.Form):
    cod_registro=forms.CharField(required=True)
    
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)



    def clean_codregistro(self):
        codigo=self.cleaned_data['cod_registro']

        if len(codigo)==6:
            #verificamos que el codigo y el id del usuario sean validos
            activo=User.objects.cod_validar(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('Codigo incorrecto')

        else:
            raise forms.ValidationError('Codigo incorrecto')

       

            

    
