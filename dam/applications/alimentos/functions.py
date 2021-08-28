from .models import Alimento

def cal_x_gramo(lista):
        lista_obj_alimentos=[]
        lista_cal_gramo_alimentos=[]

        for i in lista:
            al=Alimento.objects.get(pk=i)
            lista_obj_alimentos.append(al)
            calorias_gramo=((al.calorias)/1000)
            lista_cal_gramo_alimentos.append(calorias_gramo)

        return lista_obj_alimentos,lista_cal_gramo_alimentos

#multiplicar elementos de 2 listas diferentes
#multiplico la cantidad por la porcion
#por algun arte oscura o mistica tengo q preguntar si existen n1 y n2
    
def cant_x_porcion(lista1,lista2):
    lista_cantidad_x_porcion=[]
    for num1, num2 in zip(lista1, lista2):
        if num1 and num2:
            lista_cantidad_x_porcion.append(int(num1) * int(num2))
    return lista_cantidad_x_porcion

#multiplico la porcion en gramos por las cal x gramo
#para obtener el total de cal en cada alimento

def total_cal(lista1,lista2):
        lista_total_cal=[]
        for num1, num2 in zip(lista1, lista2):
            if num1 and num2:
	            lista_total_cal.append(int(num1) * int(num2))

        return lista_total_cal