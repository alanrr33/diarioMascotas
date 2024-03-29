from rest_framework.generics import ListAPIView

from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.edit import (CreateView, 
                                        FormView)
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import (reverse_lazy,
                            reverse)
from django.http.response import HttpResponseRedirect

from .forms import (DiarioForm,
                    EditarAlimentoForm)
from .models import (Alimento,
                    AlimentoConsumido)
from applications.diario.models import Diario

from .functions import (cal_x_gramo,
                        total_cal,
                        limpiar_lista)
from .serializers import AlimentoSerializer,AlimentoConsumidoSerializer
from .filters import AlimentoFilter



# Create your views here.

class BuscarAlimentos(LoginRequiredMixin,FormView,ListView):
    form_class=DiarioForm
    template_name="alimentos/buscar_alimento.html"
    filterset_class=AlimentoFilter
    #volver a detalle diario
    success_url=reverse_lazy('diario_urls:detallediario')

    #listview
    model = Alimento
    paginate_by=4
    ordering='nombre'
    context_object_name="alimentos"

    
    def get_queryset(self):
        #busqueda=self.request.GET.get('busqueda')
        diario_pk=self.kwargs['pk']
        diario=Diario.objects.get(pk=diario_pk)
        tipomascota=diario.mascota.tipo
        print('tipo mascota = %s' %tipomascota)
        query=Alimento.objects.all().filter(tipo_mascota=tipomascota)


        """if not busqueda:
            busqueda=""
        resultado=Alimento.objects.buscar_alimentos(busqueda).filter(tipo_mascota=tipomascota)
        return resultado"""

        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=query)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diario_pk=self.kwargs['pk']
        context["diario"]=Diario.objects.get(pk=diario_pk)

        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context

    def form_valid(self, form):
        #objetos
        alimentos =limpiar_lista(self.request.POST.getlist('cb_alimento'))   

        #preciso objetos diario y alimento para poder insertarlo en la db
        diarioid=self.kwargs['pk']
        diario_obj=Diario.objects.get(pk=diarioid)
        self.pk=diarioid

        cantidad_clean=limpiar_lista(self.request.POST.getlist('cantidad'))
        print (cantidad_clean)


        #calculos auxiliares
        #listas clean
        #obtener las calorias de cada alimento chequeado
        lista_obj_alimentos,lista_cal_gramo_alimentos=cal_x_gramo(alimentos)
        lista_total_cal=total_cal(cantidad_clean,lista_cal_gramo_alimentos)

        alimentosConsumidos=[]

   
        if ((len(cantidad_clean)) == (len(lista_obj_alimentos))):

            for i in (range(len(alimentos))):
                alimentoconsumido=AlimentoConsumido(
                    alimento=lista_obj_alimentos[i],
                    diario=diario_obj,
                    cantidad=cantidad_clean[i],
                    total_cal=lista_total_cal[i],
                )
                alimentosConsumidos.append(alimentoconsumido)
            
            for i in range(len(alimentos)):
                diario_obj.total_cal+=lista_total_cal[i]
                diario_obj.save()

            AlimentoConsumido.objects.bulk_create(
            alimentosConsumidos
            )

            if (len(lista_obj_alimentos))==1:

                messages.success(self.request,"El alimento ha sido agregado con exito")
            else:
                messages.success(self.request,"Los alimentos han sido agregados con exito")

        else:
            #print('algo vino vacio o hay alguna diferencia en el largo')
            #print(len(cantidad_clean))
            #print(len(lista_obj_alimentos))
            messages.warning(self.request,"Para agregar los elementos debe completar todos sus campos!")
        
        return super(BuscarAlimentos, self).form_valid(form)

    def get_success_url(self):
         return reverse('diario_urls:detallediario', kwargs={'pk': self.pk})

class ListaAlimentos(LoginRequiredMixin,ListView):
    #detail view
    template_name="alimentos/lista_alimentos.html"
    context_object_name="alimentos"
    paginate_by=5
    ordering='nombre'
    model=Alimento

    def get_queryset(self):
        return Alimento.objects.buscar_alimentos_creadopor(self.request.user).order_by('nombre')


class AgregarAlimento(LoginRequiredMixin,CreateView):
    template_name="alimentos/agregar_alimento.html"
    model=Alimento
    fields=['nombre','marca','descripcion','calorias','tipo_mascota']
    success_url=reverse_lazy('alimentos_urls:listaalimentos')

    def form_valid(self, form):
        print('###FORM VALID###')
        print(self.request.user)
        alimento=form.save(commit=False)
        alimento.creada_por=self.request.user
        alimento.save()
        return super(AgregarAlimento,self).form_valid(form)

class BorrarAlimento(LoginRequiredMixin,TemplateView):
    #model=Alimento
    template_name="alimentos/eliminar_alimento.html"
    #success_url=reverse_lazy('alimentos_urls:listaalimentos')

    def dispatch(self, request, *args, **kwargs):
        #solo dueño puede eliminar alimento suyo
        alimento=Alimento.objects.get(pk=self.kwargs['pk'])

        if alimento.creada_por != self.request.user:
            messages.warning(self.request, 'Que hacemos metiendo mano en la url ?')
            return HttpResponseRedirect(reverse('alimentos_urls:listaalimentos'))
            #messages.success(self.request, 'Bienvenido!')

        return super(BorrarAlimento, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args,**kwargs):
        print('##GET eliminaralimentousuario##')
        alimento=Alimento.objects.get(pk=self.kwargs['pk'])
        #guardo el id del diario en una variable ya que voy a borrar el alimento de la db

        if alimento:
            alimento.delete()
            print('borrado')
            return HttpResponseRedirect(reverse('alimentos_urls:listaalimentos'))

        return super(BorrarAlimento,self).get(request, *args, **kwargs)
    

class EditarAlimento(LoginRequiredMixin,FormView):
    template_name="alimentos/editar_alimento.html"
    form_class=EditarAlimentoForm
    
    success_url=reverse_lazy('alimentos_urls:listaalimentos')

    def dispatch(self, request, *args, **kwargs):
        #solo dueño puede editar alimento del diario de su mascota
        alimento=Alimento.objects.get(pk=self.kwargs['pk'])


        if alimento.creada_por != self.request.user:
            messages.warning(self.request, 'Que hacemos metiendo mano en la url ?')
            return HttpResponseRedirect(reverse('alimentos_urls:listaalimentos'))
            #messages.success(self.request, 'Bienvenido!')

        return super(EditarAlimento, self).dispatch(request, *args, **kwargs)



    def form_valid(self, form):
        alimento=Alimento.objects.get(pk=self.kwargs['pk'])
        
        #update
        print("##POST editar alimento usuario##")

        if form.cleaned_data['nombre'] == alimento.nombre:
            print ('son iguales')
        else:
            print('no lo son, es {} y el form es {}'.format(alimento.nombre,form.cleaned_data['nombre']))
            alimento.nombre=form.cleaned_data['nombre']
            alimento.save()
        
        if form.cleaned_data['marca'] == alimento.marca:
            print ('son iguales')
        else:
            print('no lo son, es {} y el form es {}'.format(alimento.marca,form.cleaned_data['marca']))
            alimento.marca=form.cleaned_data['marca']
            alimento.save()
        
        if form.cleaned_data['descripcion'] == alimento.descripcion:
            print ('son iguales')
        else:
            print('no lo son, es {} y el form es {}'.format(alimento.descripcion,form.cleaned_data['descripcion']))
            alimento.descripcion=form.cleaned_data['descripcion']
            alimento.save()
        
        if form.cleaned_data['calorias'] == alimento.calorias:
            print ('son iguales')
        else:
            print('no lo son, es {} y el form es {}'.format(alimento.calorias,form.cleaned_data['calorias']))
            alimento.calorias=form.cleaned_data['calorias']
            alimento.save()
        

        return super(EditarAlimento,self).form_valid(form)
    
    """def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #comida=AlimentoConsumido.objects.get(pk=self.kwargs['pk'])
        comida=Alimento.objects.get(pk=self.kwargs['pk'])
        self.pk=comida.diario.id
        context['diario'] =Diario.objects.get(pk=self.pk) 
        return context"""
    #que hacía esto? solo un hechicero podría saberlo
    
    #sobreescribimos el metodo para obtener los kwargs del form para poder pasar la id al modelform
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs
    
    

    def get_success_url(self):
         return reverse('alimentos_urls:listaalimentos')


"APIS"

#Alimento
class BuscarAlimentoListApiView(ListAPIView):
    serializer_class=AlimentoSerializer

    def get_queryset(self):
        kword=self.request.query_params.get('kword','')

        return Alimento.objects.filter(
            nombre__icontains=kword
        ).order_by('nombre')

#ALimento Consumido

class AlimentoConsumidoListApiView(ListAPIView):
    serializer_class=AlimentoConsumidoSerializer

    def get_queryset(self):
        kword=self.request.query_params.get('kword','')

        return AlimentoConsumido.objects.filter(
            id__icontains=kword
        ).order_by('id')
    