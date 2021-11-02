from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import User
from .functions import hay_numeros

class UserRegisterForm(forms.ModelForm):

    GENDER_CHOICES=(
        ('M','Masculino'),
        ('F','Femenino'),
        ('O','Otro'),
    )



    nombre=forms.CharField(
         
        label='Nombre',
        max_length=30,
        required=True,
        help_text='Ingrese su nombre',
        widget=forms.TextInput(
        
        attrs={
            'placeholder':'Luis Alberto',
        }
    ))

    apellido=forms.CharField(
         
        label='Apellido',
        max_length=30,
        required=True,
        help_text='Ingrese su apellido',
        widget=forms.TextInput(

        attrs={
            'placeholder':'Jade Spinetta',
        }
    ))

    genero=forms.ChoiceField(
        choices=GENDER_CHOICES, 
        label='Genero',
        required=True,
        widget=forms.Select(

        attrs={
            
        }
    ))

    email=forms.EmailField(
         
        label='Email',
        required=True,
        help_text='Ingrese su dirección de email',
        widget=forms.EmailInput(

        attrs={
            'placeholder':'luisalberto@pepe.com',
        }
    ))

    username=forms.CharField(
         
        label='Usuario',
        min_length=5,
        max_length=20,
        required=True,
        help_text='Nombre de usuario para poder acceder al sitio',
        widget=forms.TextInput(

        attrs={
            'placeholder':'Nombre de usuario',
        }
    ))

    password1=forms.CharField(
        min_length=5,
        label='Contraseña', 
        required=True,
        help_text='Ingrese una contraseña',
        widget=forms.PasswordInput(
        attrs={
            'placeholder':'Contraseña'
        }
    ))

    password2=forms.CharField(
        min_length=5,
        label='Contraseña', 
        required=True, 
        help_text='Repita la contraseña',
        widget=forms.PasswordInput(
        attrs={
            'placeholder':'Repetir Contraseña'
        }
    ))



    class Meta:
        model=User

        fields=(
            'nombre',
            'apellido',
            'genero',
            'email',
            'username',
            
        )


        


    #al hacer validacion de varios campos debemos sobreescribir el metodo clean
    def clean(self):
        cleaned_data=super(UserRegisterForm, self).clean()
        email = self.cleaned_data.get('email')
        password1=self.cleaned_data['password1']
        password2=self.cleaned_data['password2']
        username=self.cleaned_data['username']
        nombre=self.cleaned_data['nombre']
        apellido=self.cleaned_data['apellido']

        if email:
            if not email.endswith('.com'):
                self.add_error('email',"Solo emails terminados en .com estan permitidos")
            if User.objects.filter(email=email).exists():
                self.add_error('email',"El email ya se encuentra en uso")


        

        if nombre:
            x=hay_numeros(nombre)
            if x==True:
                self.add_error('nombre','Hay numeros en el nombre')
            
        
        if apellido:
            x=hay_numeros(apellido)
            if x==True:
                self.add_error('apellido','Hay numeros en el apellido')
        
        if password1:
            if (len(password1)<6):
                self.add_error('password1','La contraseña debe tener al menos 6 caracteres')
            if not any (c.isupper() for c in password1):
                self.add_error('password1','La contraseña debe contener al menos 1 caracter en mayuscula')
            if not any(c.islower() for c in password1):
                self.add_error('password1','La contraseña debe tener al menos 1 caracter en miniscula')
            if not any (c.isdigit() for c in password1):
                self.add_error('password1','La contraseña debe tener al menos un caracter numerico')

        if password1 and password2:
            if password1 != password2:
                self.add_error('password2','Las contraseñas no coinciden')
            

        if username and nombre:
            if username==nombre:
                self.add_error('nombre','El nombre no puede ser el mismo que username')


        return cleaned_data
    

class LoginForm(forms.Form):

    username=forms.CharField(label='Usuario', required=True, widget=forms.TextInput(
        attrs={
            'placeholder':'Usuario',
            
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



    def clean_cod_registro(self):
        codigo=self.cleaned_data['cod_registro']

        if len(codigo) == 6:
            #verificamos que el codigo y el id del usuario sean validos
            activo=User.objects.cod_validar(
                self.id_user,
                codigo
            )
            if not activo:
                print('codigo incorrecto %s' % codigo)
                raise forms.ValidationError('Codigo incorrecto')

        else:
            print('codigo incorrecto %s' % codigo)
            raise forms.ValidationError('Codigo incorrecto')

class ReestablecerPassForm(forms.Form):
    email=forms.EmailField(
        required=True,
        help_text='Ingrese la direccion de email con la que se registro',
        widget=forms.EmailInput(
        attrs={
        'placeholder':'luis@gmail.com'
        }

        ))

    def clean(self):
        cleaned_data=super(ReestablecerPassForm, self).clean()

        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            print('miau')
        else:
           self.add_error('email','No hay ningun usuario registrado con este email')

        return cleaned_data

class PanelUsuarioForm(forms.Form):
    password1=forms.CharField(
        min_length=5,
        label='Contraseña', 
        required=True,
        help_text='Ingrese una contraseña nueva',
        widget=forms.PasswordInput(
        attrs={
            'placeholder':'Contraseña'
        }
    ))

    password2=forms.CharField(
        min_length=5,
        label='Contraseña', 
        required=True, 
        help_text='Repita la contraseña nueva',
        widget=forms.PasswordInput(
        attrs={
            'placeholder':'Repetir Contraseña'
        }
    ))


    class Meta:
        model=User

        fields=(
            'genero',
        )

    def clean(self):
        cleaned_data=super(PanelUsuarioForm, self).clean()

        password1=self.cleaned_data['password1']
        password2=self.cleaned_data['password2']

        if password1:
            if (len(password1)<6):
                self.add_error('password1','La contraseña debe tener al menos 6 caracteres')
            if not any (c.isupper() for c in password1):
                self.add_error('password1','La contraseña debe contener al menos 1 caracter en mayuscula')
            if not any(c.islower() for c in password1):
                self.add_error('password1','La contraseña debe tener al menos 1 caracter en miniscula')
            if not any (c.isdigit() for c in password1):
                self.add_error('password1','La contraseña debe tener al menos un caracter numerico')

        if password1 and password2:
            if password1 != password2:
                self.add_error('password2','Las contraseñas no coinciden')
        


        return cleaned_data
       

            

    
