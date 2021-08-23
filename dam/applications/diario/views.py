from datetime import datetime, timedelta

from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from django.shortcuts import redirect

from .models import Diario
from .forms import EditarAlimentoForm,CompletarDiarioForm

from applications.alimentos.models import AlimentoConsumido
from applications.mascotas.models import Mascota,PesoMascotaDiario

# Create your views here.

class VerDiarios(LoginRequiredMixin,ListView):
    template_name="diario/ver_diarios.html"
    model = Diario
    context_object_name='lista_diario'
    paginate_by=4

    def dispatch(self, request, *args, **kwargs):
        #Asegurandome que solo los dueños de las mascotas puedan ver los diarios de sus mascotas 
        mascota=Mascota.objects.get(pk=self.kwargs.get('pk'))

        if mascota.dueño != self.request.user:
            messages.warning(self.request, 'Que hacemos metiendo mano en la url ?')
            return HttpResponseRedirect(reverse('mascotas_urls:listarmascotas'))
        
        return super(VerDiarios, self).dispatch(request, *args, **kwargs)

    #creacion del diario a partir del boton
    def post(self, request, *args, **kwargs):
       
        print('###POST###')
        print(self.kwargs['pk'])
        fecha=self.request.POST.get('selectorFecha','')
        print('fecha ',fecha)   

        mascota=Mascota.objects.get(pk=self.kwargs['pk'])


        if fecha:
            print('hay fecha {}'.format(fecha))

            obj, created=Diario.objects.get_or_create(
            fecha=fecha,
            mascota=mascota,
            defaults={
                'mascota':mascota,
            }
            )

            #si se creo
            if created:
                print('diario creado')
                diario=Diario.objects.filter(mascota=mascota).order_by('-id')[0]
                self.pk=diario.id
                return HttpResponseRedirect(reverse('diario_urls:detallediario', kwargs={'pk': self.pk}))
            else:
                #si estaba creado
                print('ya existe un diario para esta fecha')
                return HttpResponseRedirect(reverse('diario_urls:detallediario', kwargs={'pk': obj.id}))
                
            
       
        else:
            print('no hay fecha')
            messages.info(self.request, 'Por favor introduzca una fecha valida')


        return redirect(request.build_absolute_uri())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mascota'] =Mascota.objects.get(pk=self.kwargs['pk']) 
        return context

    def get_queryset(self):
        palabra_clave=self.kwargs['pk']
        print(palabra_clave)
        return Diario.objects.buscar_diarios(palabra_clave).order_by('fecha')

class EditarAlimentoDiario(LoginRequiredMixin,FormView):
    template_name="diario/editar_alimento_diario.html"
    form_class=EditarAlimentoForm
    #success_url=reverse_lazy('diario_urls:detallediario')

    def dispatch(self, request, *args, **kwargs):
        #solo dueño puede editar alimento del diario de su mascota
        alimento=AlimentoConsumido.objects.get(pk=self.kwargs['pk'])
        diario = Diario.objects.get(pk=alimento.diario.id)
        mascota=Mascota.objects.get(pk=diario.mascota.id)

        if mascota.dueño != self.request.user:
            print(diario.id)
            messages.warning(self.request, 'Que hacemos metiendo mano en la url ?')
            return HttpResponseRedirect(reverse('mascotas_urls:listarmascotas'))
            #messages.success(self.request, 'Bienvenido!')

        return super(EditarAlimentoDiario, self).dispatch(request, *args, **kwargs)



    def form_valid(self, form):

        print("##POST##")
        
        cantidad=form.cleaned_data['cantidad']
        porcion=form.cleaned_data['porcion']
        comida=AlimentoConsumido.objects.get(pk=self.kwargs['pk'])
        self.pk=comida.diario.id

        if cantidad != comida.cantidad:
            print('no son iguales, es {} y el form es {}'.format(comida.cantidad,form.cleaned_data['cantidad']))
            comida.cantidad=cantidad
            comida.save()
        else:
            print ('son iguales cantidad')

        if porcion != comida.porcion:
            print('no lo son, es {} y el form es {}'.format(comida.porcion,form.cleaned_data['porcion']))
            comida.porcion=porcion
            comida.save()
        else:
            print('son iguales porcion')
            

        return super(EditarAlimentoDiario,self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comida=AlimentoConsumido.objects.get(pk=self.kwargs['pk'])
        self.pk=comida.diario.id
        context['diario'] =Diario.objects.get(pk=self.pk) 
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs
    
    

    def get_success_url(self):
         return reverse('diario_urls:detallediario', kwargs={'pk': self.pk})


class EliminarAlimentoDiario(LoginRequiredMixin,TemplateView):
    template_name="diario/eliminar_alimento_diario.html"

    def dispatch(self, request, *args, **kwargs):
        #solo dueño puede eliminar alimento del diario de su mascota
        alimento=AlimentoConsumido.objects.get(pk=self.kwargs['pk'])
        diario = Diario.objects.get(pk=alimento.diario.id)
        mascota=Mascota.objects.get(pk=diario.mascota.id)

        if mascota.dueño != self.request.user:
            print(diario.id)
            messages.warning(self.request, 'Que hacemos metiendo mano en la url ?')
            return HttpResponseRedirect(reverse('mascotas_urls:listarmascotas'))

        return super(EliminarAlimentoDiario, self).dispatch(request, *args, **kwargs)



    def get(self, request, *args,**kwargs):
        print('##GET eliminaralimentodiario##')
        alimento=AlimentoConsumido.objects.get(pk=self.kwargs['pk'])
        #guardo el id del diario en una variable ya que voy a borrar el alimento de la db
        diarioid=alimento.diario.id

        if alimento:
            print(alimento.diario.id)
            alimento.delete()
            print('borrado')
            return HttpResponseRedirect(reverse('diaro_urls:detallediario',kwargs={'pk':diarioid}))

        return super(EliminarAlimentoDiario,self).get(request, *args, **kwargs)

    #en caso de q quiera volver a usar el delete view
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comida=AlimentoConsumido.objects.get(pk=self.kwargs['pk'])
        self.pk=comida.diario.id
        #context['diario'] =Diario.objects.get(pk=self.pk) 
        return context

    def get_success_url(self):
         return reverse('diario_urls:detallediario', kwargs={'pk': self.kwargs['diariopk']})"""

class DetalleDiario(LoginRequiredMixin,FormView,TemplateView):

    #formview
    form_class=CompletarDiarioForm
    template_name="diario/detalle_diario.html"
    #volver a detalle diario
    success_url=reverse_lazy('diario_urls:detallediario')

    def dispatch(self, request, *args, **kwargs):
        #Asegurandome que solo los dueños de las mascotas puedan ver los diarios de sus mascotas
        diario = Diario.objects.get(pk=self.kwargs.get('pk'))
        mascota=Mascota.objects.get(pk=diario.mascota.id)

        if mascota.dueño != self.request.user:
            messages.warning(self.request, 'Que hacemos metiendo mano en la url ?')
            return HttpResponseRedirect(reverse('mascotas_urls:listarmascotas'))
        #messages.success(self.request, 'Bienvenido!')
        
        return super(DetalleDiario, self).dispatch(request, *args, **kwargs)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diario=Diario.objects.get(pk=self.kwargs.get('pk'))
       
        context["diario"] = diario
        context['mascota']=Mascota.objects.get(pk=diario.mascota.id)
        context['comidas']=AlimentoConsumido.objects.buscar_alimentos_consumidos_fk(self.kwargs.get('pk'))
        return context

    def get(self, request, *args,**kwargs):
        print('##GET##')
        diario = Diario.objects.get(pk=self.kwargs.get('pk'))
        mascota=Mascota.objects.get(pk=diario.mascota.id)
        valor=self.request.GET.get('ir','')

        if valor=="atras":
            print('vamos atras')
            diarioayer=diario.fecha-timedelta(days=1)
            

            obj, created=Diario.objects.get_or_create(
            fecha=diarioayer,
            mascota=mascota,
            defaults={
                'mascota':mascota,
            }
            )

            if created:
                print('diario creado')
                diario=Diario.objects.get(mascota=mascota,fecha=diarioayer)
                return HttpResponseRedirect(reverse('diario_urls:detallediario', kwargs={'pk': diario.id}))
            else:
                #si estaba creado
                print('ya existe un diario para esta fecha')
                return HttpResponseRedirect(reverse('diario_urls:detallediario', kwargs={'pk': obj.id}))



        if valor=="adelante":
            print('vamos adelante')
            print(diario)
            diarioman=diario.fecha+timedelta(days=1)
            

            obj, created=Diario.objects.get_or_create(
            fecha=diarioman,
            mascota=mascota,
            defaults={
                'mascota':mascota,
            }
            )

            if created:
                print('diario creado mañana')
                diario=Diario.objects.get(mascota=mascota,fecha=diarioman)
                return HttpResponseRedirect(reverse('diario_urls:detallediario', kwargs={'pk': diario.id}))
            else:
                #si estaba creado
                print('ya existe un diario para esta fecha')
                return HttpResponseRedirect(reverse('diario_urls:detallediario', kwargs={'pk': obj.id}))

        return super(DetalleDiario,self).get(request, *args, **kwargs)


    def form_valid(self, form):
        print("##FORM VALID##")
        diario = Diario.objects.get(pk=self.kwargs.get('pk'))
        mascota=Mascota.objects.get(pk=diario.mascota.id)
        completar=self.request.POST.get('completar','')
        dif_cal=self.request.POST.get('difcal','')
        diario_obj=Diario.objects.get(pk=self.kwargs['pk'])
        peso_dia=self.request.POST.get('peso','')
        

        if completar=="completar":
            print('completar diario')

            obj, created=PesoMascotaDiario.objects.update_or_create(
            mascota=mascota,
            fecha=diario.fecha,
            
            defaults={
                'mascota':mascota,
                'fecha':diario.fecha,
                'peso':peso_dia,
            }
            )

            if created:
                messages.success(self.request, 'Creada entrada de peso para la mascota')          
            else:
                #si estaba creado se actualiza
                messages.success(self.request, 'Peso actualizado con exito a %s kg ' % obj.peso)    




            diario_obj.completado=True
            diario_obj.dif_cal=dif_cal
            diario_obj.save()
        elif completar=="modificar":
            print("modificar diario")
            diario_obj.completado=False
            diario_obj.save()

        return super(DetalleDiario, self).form_valid(form)

    
    def get_success_url(self):
         #print(self.kwargs.get('pk'))
         return reverse('diario_urls:detallediario', kwargs={'pk': self.kwargs.get('pk')})

        