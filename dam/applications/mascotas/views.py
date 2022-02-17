from datetime import datetime, timedelta

from rest_framework.generics import ListAPIView

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.generic.list import ListView

from django.http import HttpResponseRedirect

import django_excel as excel

from django.contrib import messages
from django.views.generic import (
                                ListView,
                                DeleteView,
                                TemplateView
                                )
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse


from applications.diario.models import Diario
from .forms import (
                    MascotaRegisterForm,
                    MascotaUpdateForm,
                    AgregarNotaForm,
                    )
from .models import (
                    Mascota,
                    PesoMascotaDiario,
                    Nota
                    )
from .functions import generar_grafico
from .filters import NotaFilter
from .serializers import MascotaSerializer

# Create your views here.

#preciso estar logueado para añadir mascota


class MascotaRegisterView(LoginRequiredMixin,FormView):
    template_name="mascotas/registrar.html"
    form_class=MascotaRegisterForm
    success_url=reverse_lazy('mascotas_urls:listarmascotas')

    def form_valid(self, form):
        dueño=self.request.user
        nombre=form.cleaned_data['nombre']
        tipo=form.cleaned_data['tipo']
        edad=int(form.cleaned_data['edad'])
        peso=form.cleaned_data['peso']
        actividad=form.cleaned_data['actividad']
        tamaño=form.cleaned_data['tamaño']
        esterilizado=form.cleaned_data['esterilizado']
        objetivo=form.cleaned_data['objetivo']
        imagen=form.cleaned_data['imagen']

        
        Mascota.objects.create_mascota(
            
            dueño=dueño,
            nombre=nombre,
            tipo=tipo,
            edad=edad,
            peso=peso,
            actividad=actividad,
            tamaño=tamaño,
            esterilizado=esterilizado,
            objetivo=objetivo,
            imagen=imagen,
        )
        
        return super(MascotaRegisterView,self).form_valid(form)

class PanelMascotaView(LoginRequiredMixin,TemplateView):
    template_name="mascotas/panel.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mascota'] =Mascota.objects.get(pk=self.kwargs['pk']) 
        return context
    
class ListarMascotasView(LoginRequiredMixin,ListView):
    template_name ="mascotas/listarmascotas.html"
    model = Mascota
    paginate_by=3
    ordering='nombre'
    context_object_name='lista_mascotas'
    

    def get_queryset(self):
        
        return Mascota.objects.buscar_mascota_dueñoid(self.request.user.id).order_by('nombre')


class UpdateMascotaView(LoginRequiredMixin,FormView):
    template_name="mascotas/editar.html"
    form_class=MascotaUpdateForm
    success_url=reverse_lazy('mascotas_urls:listarmascotas')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        mascota=Mascota.objects.get(pk=self.kwargs['pk'])

        nombre=form.cleaned_data['nombre']
        tipo=form.cleaned_data['tipo']
        edad=form.cleaned_data['edad']
        peso=form.cleaned_data['peso']
        actividad=form.cleaned_data['actividad']
        tamaño=form.cleaned_data['tamaño']
        esterilizado=form.cleaned_data['esterilizado']
        objetivo=form.cleaned_data['objetivo']
        imagen=form.cleaned_data['imagen']

        if nombre!=mascota.nombre:
            print('campo nombre con diferencias')
            mascota.nombre=nombre
            messages.success(self.request, 'Nombre cambiado con exito!')

        if tipo!=mascota.tipo:
            print('campo tipo con diferencias')
            mascota.tipo=tipo
            messages.success(self.request, 'Tipo de mascota cambiado con exito!')

        if edad!=mascota.edad:
            print('campo edad con diferencias')
            mascota.edad=edad
            messages.success(self.request, 'Edad cambiado con exito!')

        if peso!=mascota.peso:
            print('campo peso con diferencias')
            mascota.peso=peso
            messages.success(self.request, 'Peso cambiado con exito!')

        if actividad!=mascota.actividad:
            print('campo actividad con diferencias')
            mascota.actividad=actividad
            messages.success(self.request, 'Actividad cambiada con exito!')

        if tamaño!=mascota.tamaño:
            print('campo tamaño con diferencias')
            mascota.tamaño=tamaño
            messages.success(self.request, 'Tamaño cambiado con exito!')

        if esterilizado!=mascota.esterilizado:
            print('campo esterilizado con diferencias')
            mascota.esterilizado=esterilizado
            messages.success(self.request, 'Esterilizado cambiado con exito!')

        if objetivo!=mascota.objetivo:
            print('campo objetivo con diferencias')
            mascota.objetivo=objetivo
            messages.success(self.request, 'Objetivo cambiado con exito!')
        
        if imagen:
            print('imagen cambiada')
            mascota.imagen=imagen
            messages.success(self.request, 'Imagen cambiada con exito!')

        
        mascota.save()


        
        
        return super(UpdateMascotaView,self).form_valid(form)

class DeleteMascotaView(LoginRequiredMixin,DeleteView):
    template_name="mascotas/eliminar.html"
    model=Mascota
    success_url=reverse_lazy('mascotas_urls:listarmascotas')

class ReportesMascotaView(LoginRequiredMixin,TemplateView):
    template_name="mascotas/reportes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mascota=Mascota.objects.get(pk=self.kwargs['pk'])
        context['mascota'] =mascota

        dias=7
        tipografico=self.request.GET.get('selectTipo')
        print(tipografico)

        if (self.request.GET.get('selectDias') != None):
            dias=int(self.request.GET.get('selectDias'))
            

        if tipografico=="calorias":
            if dias != None:
                graph_div=generar_grafico(mascota,tipografico,dias)
                context["graph_div"]=graph_div

        elif tipografico=="peso":
            if dias != None:
                graph_div=generar_grafico(mascota,tipografico,dias)
                context["graph_div"]=graph_div

        return context
    
# generar el reporte en memoria y devolverlo a traves de una http response
def listresults(request,pk):
    
    tipografico=request.POST.get('selectTipo','')
    cantdias=int(request.POST.get('selectDias',''))
    formato=request.POST.get('selectFormato','')
    mascota=Mascota.objects.get(pk=pk)

    print('tipo de grafico {}, cantidad dias {}, formato: {}'.format(tipografico,cantdias,formato))

    # Definir los datos en una lista
    export = [] 

    if tipografico=='calorias':
        # Se obtienen los datos del model y se agregan a la lista
        diarios=Diario.objects.filter(mascota=mascota,fecha__gte=datetime.now()-timedelta(days=cantdias)).order_by('fecha')
        if diarios:
            export.append(['Fecha', 'Calorias'])
            #formateamos la fecha al estilo "25-09-1996"
            for diario in diarios:
                export.append(["{0:%d-%m-%Y}".format(diario.fecha), diario.total_cal])
                

    if tipografico=='peso':
        pesos=PesoMascotaDiario.objects.filter(mascota=mascota,fecha__gte=datetime.now()-timedelta(days=cantdias)).order_by('fecha')
        if pesos:
            export.append(['Fecha', 'Peso (kg)'])
            #formateamos la fecha al estilo "25-09-1996"
            for i in pesos:
                export.append(["{0:%d-%m-%Y}".format(i.fecha),float(i.peso)])

    #obtenemos la fecha de hoy para añadirla al archivo

    fechahoy    = datetime.now()
    strFechahoy = fechahoy.strftime("%d%m%Y")
    
    # Transcribir la data a una hoja de calculo en memoria
    sheet = excel.pe.Sheet(export)

    # Generar el archivo desde la hoja en memoria con 
    # un nombre de archivo que se recibira en el navegador

    if formato == "csv":
        return excel.make_response(sheet, "csv", file_name="Reporte-"+strFechahoy+".csv")
    elif formato == "ods":
        return excel.make_response(sheet, "ods", file_name="Reporte-"+strFechahoy+".ods")
    elif formato == "xlsx":
        return excel.make_response(sheet, "xlsx", file_name="Reporte-"+strFechahoy+".xlsx")
    else:
        messages.warning(request, 'formato {} no soportado'.format(formato))


class AgregarNotaView(LoginRequiredMixin,FormView):
    template_name="mascotas/notas.html"
    form_class=AgregarNotaForm

    def form_valid(self, form):
        mascota_id=self.kwargs['pk']
        
        mascota=Mascota.objects.get(pk=mascota_id)
        print('mascota id {}, mascota : {}'.format(mascota_id,mascota))

        fecha=form.cleaned_data['fecha']
        importancia=form.cleaned_data['importancia']
        texto=form.cleaned_data['texto']

        print('fecha: {} importancia {} texto {}'.format(fecha,importancia,texto))

        Nota.objects.create(
            mascota=mascota,
            fecha=fecha,
            importancia=importancia,
            texto=texto

        )

        return HttpResponseRedirect(
            reverse(
                'mascotas_urls:perfil',
                kwargs={'pk': mascota_id}
            )
        )
    
    

class PerfilMascotaView(LoginRequiredMixin,ListView):
    template_name ="mascotas/perfilmascota.html"
    filterset_class=NotaFilter
    paginate_by=3
    context_object_name='notas'
    #ordering='-fecha'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mascota'] =Mascota.objects.get(pk=self.kwargs['pk'])

        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        mascota=Mascota.objects.get(pk=self.kwargs['pk'])
        query=Nota.objects.filter(mascota=mascota).order_by('fecha').exclude(archivado=True)

        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=query)
        # Return the filtered queryset
        return self.filterset.qs.distinct()


#uso una vista en forma de funcion para archivar la nota ya que no necesita otra pagina
@login_required
def borrarnota(request,pk):
    
    nota=get_object_or_404(Nota,pk=pk)

    if request.method=="GET":
        nota.archivado=True
        nota.save()
        print('mascotaid %s' % nota.mascota.id)
        
        return HttpResponseRedirect(
            reverse(
                'mascotas_urls:perfil',
                kwargs={'pk': nota.mascota.id}
            )
        )



"APIS"

#Mascota
class BuscarMascotaApiView(ListAPIView):
    serializer_class=MascotaSerializer

    def get_queryset(self):
        kword=self.request.query_params.get('kword','')

        return Mascota.objects.filter(
            id__icontains=kword
        ).order_by('id')