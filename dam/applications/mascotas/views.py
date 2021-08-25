import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from datetime import datetime, timedelta

from django.contrib import messages
from django.views.generic import (ListView,
                                DeleteView,
                                TemplateView)
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from applications.diario.models import Diario
from .forms import MascotaRegisterForm,MascotaUpdateForm
from .models import Mascota,PesoMascotaDiario

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
        edad=form.cleaned_data['edad']
        peso=form.cleaned_data['peso']
        actividad=form.cleaned_data['actividad']
        tamaño=form.cleaned_data['tamaño']
        esterilizado=form.cleaned_data['esterilizado']
        objetivo=form.cleaned_data['objetivo']

        
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
            dias=float(self.request.GET.get('selectDias'))
            

        if tipografico=="calorias":
            if dias != None:
                diarios=Diario.objects.filter(mascota=mascota,fecha__gte=datetime.now()-timedelta(days=dias))
                if diarios:
                    diccionario={"Calorias":[],"Dia":[]}
                    for diario in diarios:
                        diccionario['Calorias'].append(diario.total_cal)
                        diccionario['Dia'].append(diario.fecha)
                    #print(len(diccionario))
                    
                    f=pd.DataFrame(diccionario)
                    fig = px.bar(f, x='Dia', y='Calorias',range_x=[datetime.now()-timedelta(days=dias),datetime.now()])
                    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True,tickangle=35,fixedrange=True)
                    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True,fixedrange=True)
                
                    fig.add_hline(y=mascota.meta,
                    annotation_text="Meta diaria", 
                    annotation_position="top right",
                    annotation_font_size=10,
                    annotation_font_color="orange"
                    )

                    graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div",config= {'displaylogo': False,'displayModeBar': False,})
                    context["graph_div"]=graph_div
        else:
            if tipografico=="peso":
                if dias != None:
                    print ('tipo de grafico: %s' %tipografico)
                    pesos=PesoMascotaDiario.objects.filter(mascota=mascota,fecha__gte=datetime.now()-timedelta(days=dias)).order_by('-fecha')
                    if pesos:
                        print ('pesos: %s' %pesos[0].peso)
                        dic_peso={"Peso":[], "Dia":[]}

                        for i in pesos:
                            dic_peso['Peso'].append(i.peso)
                            dic_peso['Dia'].append(i.fecha)
                        
                        #print ('diccionario de pesos: %s' %dic_peso)

                        df=pd.DataFrame(dic_peso)
                        print ('dataframe: %s' %df)

                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=df['Dia'], y=df['Peso'],
                        mode='lines+markers',
                        name='lines+markers'))


                        graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div",config= {'displaylogo': False,'displayModeBar': False,})
                        context["graph_div"]=graph_div
                        



        return context



    