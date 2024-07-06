from funciones import *
from os import *


lista_proyectos = parse_csv('Proyectos.csv')
inicializar_id(lista_proyectos)
if lista_proyectos:
    lista_proyectos = normalizar_datos(lista_proyectos)
else:
    print("No se pudo cargar la lista de proyectos.")
    exit()

def menu():
    while True:
        imprimir_menu()
        opcion = int(input('Elija una opción: '))
        system('cls')
        match opcion:
            case 1:
                incrementar_id()
                ingresar_proyecto(lista_proyectos)
            case 2:
                mostrar_proyectos(lista_proyectos)
                modificar_proyecto(lista_proyectos)
                print('EL PROYECTO SE MODIFICO CORRECTAMENTE')
                
            case 3:
                mostrar_proyectos(lista_proyectos)
                if modificar_estado(lista_proyectos):
                    print('PROYECTO FINALIZADO CORRECTAMENTE')
            case 4:
                comprobar_proyectos(lista_proyectos)
            case 5:
                mostrar_proyectos(lista_proyectos)
            case 6:
                calcular_promedio_presupuesto(lista_proyectos)
            case 7:
                if buscar_proyecto_por_nombre(lista_proyectos):
                    print('SE ENCONTRO EL PROYECTO BUSCADO')
            case 8:
                if ordenar_asc_desc_proyectos(lista_proyectos):
                    print(lista_proyectos)
                    print('PROYECTO ORDENADO CORRECTAMENTE')
            case 9:
                retomar_proyecto(lista_proyectos)                    
            case 10:                
                if ordenar_proyectos_por_fecha(lista_proyectos):
                    print('PROYECTOS ORDENADOS CORRECTAMENTE POR SU FECHA DE INICIO')
            case 11:
                generar_reporte_presupuesto(lista_proyectos)
                print('REPORTE PRESUPUESTARIO GENERADO CORRECTAMENTE')
            case 12:
                generar_reporte_nombre(lista_proyectos)
            case 13:
                generar_json_finalizados(lista_proyectos, 'Proyectos_finalizados')
            case 14:
                promedio_presupuesto_cancelados_desarrollo(lista_proyectos)
            case 15:
                menor_presupuesto_finalizados(lista_proyectos, 'Presupuesto')
            case 16:
                actualizar_csv(lista_proyectos, 'Proyectos.csv')
                print('SALIENDO DEL SISTEMA')
                break

