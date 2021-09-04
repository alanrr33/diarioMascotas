from datetime import datetime, timedelta

import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

import django_excel as excel

from applications.diario.models import Diario
from .models import Mascota,PesoMascotaDiario


def generar_grafico(mascota,tipografico,dias):

    if tipografico=="calorias":

        diarios=Diario.objects.filter(mascota=mascota,fecha__gte=datetime.now()-timedelta(days=dias)).order_by('fecha')
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
            
            return graph_div

    elif tipografico=='peso':

        pesos=PesoMascotaDiario.objects.filter(mascota=mascota,fecha__gte=datetime.now()-timedelta(days=dias)).order_by('fecha')
        if pesos:
            #print ('pesos: %s' %pesos[0].peso)
            dic_peso={"Peso":[], "Dia":[]}

            for i in pesos:
                dic_peso['Peso'].append(i.peso)
                dic_peso['Dia'].append(i.fecha)
            
            #print ('diccionario de pesos: %s' %dic_peso)

            df=pd.DataFrame(dic_peso)
            #print ('dataframe: %s' %df)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Dia'], y=df['Peso'],
            mode='lines+markers',
            name='lines+markers'))


            graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div",config= {'displaylogo': False,'displayModeBar': False,})

            return graph_div
