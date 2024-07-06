from datetime import datetime, date
import os
import csv
import json


#ARREGLAR TEMA ID, DEBE TENER EN CUENTA LOS PROYECTOS EXISTENTES
id_auto_incremental = 0  # Defino la variable global

def incrementar_id():
    global id_auto_incremental
    id_auto_incremental +=1
    return id_auto_incremental

def decrementar_id():
    global id_auto_incremental
    id_auto_incremental -=1
    return id_auto_incremental

#Funcion para tomar los id existentes y asignarlos correctamente a futuros proyectos
def inicializar_id(lista_proyectos):
    global id_auto_incremental
    if lista_proyectos:
        id_auto_incremental = max(int(proyecto['id']) for proyecto in lista_proyectos)
    else:
        id_auto_incremental = 0
# FUNCIONES PARA EL CORRECTO FUNCIONAMIENTO DEL MENU
def imprimir_menu():
    print("\nSeleccione una opción:")
    print("1. Ingresar proyecto")
    print("2. Modificar proyecto")
    print("3. Cancelar proyecto")
    print("4. Comprobar proyecto")
    print("5. Mostrar todos los proyectos")
    print("6. Calcular presupuesto promedio")
    print("7. Buscar proyecto por nombre")
    print("8. Ordenar proyectos de formas ascendente o descendente segun su Nombre o Presupuesto")
    print("9. Retomar proyecto")
    print("10. Ordenar proyectos de formas ascendente o descendente segun su Fecha de inicio")
    print("11. Generar reporte de Presupuesto")
    print("12. Generar reporte por Nombre del Proyecto")
    print("13. Generar reporte de proyectos finalizados")
    print("14. Generar informe de presupuesto de proyectos cancelados segun su descripcion")
    print("15. Generar informe de top 3 proyectos finalizados con menor presupuesto")
    print("16. Salir")

def validar_opcion(mensaje, mensaje_error):
    opcion = input(mensaje)
    opcion = int(opcion)
    while opcion > 12 or opcion < 1:
        opcion = input(mensaje_error)
        opcion = int(opcion)
    return opcion

# FUNCION APERTURA DE ARCHIVO
def parse_csv(nombre_archivo:str): 
    lista_proyectos = [] 
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo,"r", encoding="utf-8") as archivo:
            primer_linea = archivo.readline()
            primer_linea = primer_linea.replace("\n","")
            lista_claves = primer_linea.split(",")
            
            for linea in archivo:
                linea_aux = linea.replace("\n","")
                lista_valores = linea_aux.split(",")
                diccionario_aux = {} 
                
                for i in range(len(lista_claves)):
                    diccionario_aux[lista_claves[i]] = lista_valores[i]
                
                lista_proyectos.append(diccionario_aux)
        
        return lista_proyectos
    else:
        # return False #MANEJAR EL MENSAJE DESDE EL MENU
        print("ARCHIVO NO ENCONTRADO")
# FIN FUNCION APERTURA DE ARCHIVO


# FUNCION PARA NORMALIZAR DATOS DE FECHAS Y PRESUPUESTO
def normalizar_datos(lista_proyectos):
    datos_modificados = False

    for proyecto in lista_proyectos:
        for clave, valor in proyecto.items():
            if clave == 'Fecha de inicio' or clave == 'Fecha de fin':
                try:
                    fecha_normalizada = datetime.strptime(valor, "%d-%m-%Y").strftime("%d-%m-%Y")
                    proyecto[clave] = fecha_normalizada
                    datos_modificados = True
                except ValueError:
                    print(f"Formato de fecha incorrecto para {clave}: {valor}")
            elif clave == 'Presupuesto':
                try:
                    presupuesto_normalizado = int(valor)
                    proyecto[clave] = presupuesto_normalizado
                    datos_modificados = True
                except ValueError:
                    print(f"Formato de presupuesto incorrecto: {valor}")

    if datos_modificados:
        print('Datos modificados correctamente')
    else:
        print('Hubo un error al normalizar los datos. Verifique que la lista no esté vacía o que los datos ya no se hayan normalizado anteriormente')
    
    return lista_proyectos

# FIN FUNCION PARA NORMALIZAR DATOS DE FECHAS Y PRESUPUESTO


# FUNCIONES PARA VALIDAR EL INGRESO DE DATOS:
def validar_tamanio_lista_proyectos(lista_proyectos:list):
    #Consulto si su longitud es mayor o igual a 50
    bandera = True
    if len(lista_proyectos) >= 50:
        bandera = False
    return bandera

def validar_nombre_proyecto(mensaje, mensaje_error):
    #Consulto si su longitud es 0 o mayor a 30 y si contiene caracteres no alfabeticos
    dato = input(mensaje)
    while len(dato) == 0 or len(dato) > 30 or (not dato.replace(" ", "").isalpha()):
        dato = input(mensaje_error)
    dato = dato.capitalize()
    return dato

def validar_descripcion_proyecto(mensaje, mensaje_error):
    #Valido si su longitud es 0 o mas de 200 caracteres
    dato = input(mensaje)
    while len(dato) == 0 or len(dato) > 200:
        dato = input(mensaje_error)
    dato = dato.capitalize()
    return dato

def validar_presupuesto_proyecto(mensaje, mensaje_error):
    #Valido si es un entero  y si es mayor a 500.000
    presupuesto = input(mensaje)
    while not (presupuesto.isdigit() and int(presupuesto) > 500000):
        presupuesto = input(mensaje_error)
    return int(presupuesto)

def validar_fecha(mensaje, mensaje_error):
    #primero valido su longitud, con los / deben ser de 10. Luego la paso a formato datetime
    while True:
        dato = input(mensaje + ": ")
        if len(dato) == 10:  # Se espera un formato de fecha dd/mm/yyyy
            try:
                fecha = datetime.strptime(dato, "%d/%m/%Y")
                return fecha
            except ValueError:
                print(mensaje_error)
        else:
            print(mensaje_error)

def validar_fechas(mensaje_inicio, mensaje_error_inicio, mensaje_fin, mensaje_error_fin):
    fecha_inicio = validar_fecha(mensaje_inicio, mensaje_error_inicio)
    
    # Aca lo que debo verificar primero es que pasen la validacion del formato y luego que
    # la fecha de fin no sea anterior a la fecha de inicio de proyecto. 
    while True:
        fecha_fin = validar_fecha(mensaje_fin, mensaje_error_fin)
        
        if fecha_fin > fecha_inicio:
            break
        else:
            print('ERROR! La fecha de fin no puede ser anterior a la fecha de inicio. Intente nuevamente')
    
    return fecha_inicio.strftime('%d/%m/%Y'), fecha_fin.strftime('%d/%m/%Y')

#MODIFICAR, EL ESTADO POR DEFAULT DEBE SER ACTIVO DE MANERA PREDETERMINADA
def validar_estado(mensaje, mensaje_error):
    estado = input(mensaje)

    while estado != 'activo' and estado != 'cancelado' and estado != 'finalizado':
        estado = input(mensaje_error)
        
    estado = estado.capitalize()   
    return estado

def confirmar_si_no(mensaje,mensaje_error)->bool:
    respuesta = input(mensaje)
    respuesta = respuesta.lower()
    while respuesta != "si" and respuesta != "no":
        respuesta = input(mensaje_error)
        respuesta = respuesta.lower()
    if respuesta == "si":
        return True
    else:
        return False

# FIN FUNCIONES PARA VALIDAR INGRESO DE DATOS

# FUNCIONES
#Funcion para ingresar un proyecto
def ingresar_proyecto(lista_proyectos):
    bandera = True
    if validar_tamanio_lista_proyectos(lista_proyectos):
        proyecto = {}
        id_proyecto = incrementar_id()
        proyecto["id"] = id_proyecto
        nombre = validar_nombre_proyecto("Ingrese nombre del nuevo proyecto: ", "Ingrese un nombre correcto: ")
        descripcion = validar_descripcion_proyecto("Ingrese la descripcion del nuevo proyecto: ", "Ingrese una descripcion correcta: ")
        fecha_inicio, fecha_fin = validar_fechas(
        "Ingrese la fecha de inicio del proyecto (dd/mm/yyyy): ",
        "ERROR! Ingrese una fecha válida en el formato dd/mm/yyyy: ",
        "Ingrese la fecha de fin del proyecto (dd/mm/yyyy): ",
        "ERROR! Ingrese una fecha válida en el formato dd/mm/yyyy: ")    
        presupuesto = validar_presupuesto_proyecto("Ingrese el presupuesto del proyecto: ", "Ingrese un presupuesto correcto: ")
        estado = 'Activo'
        proyecto["Nombre del Proyecto"] = nombre
        proyecto["Descripción"] = descripcion
        proyecto["Fecha de inicio"] = fecha_inicio
        proyecto["Fecha de Fin"] = fecha_fin
        proyecto["Presupuesto"] = presupuesto
        proyecto["Estado"] = estado
        mostrar_proyecto(proyecto,"PROYECTO\nID | NOMBRE DEL PROYECTO| DESCRIPCION | FECHA DE INICIO | FECHA DE FIN | PRESUPUESTO | ESTADO |\n")
        if confirmar_si_no("¿Desea ingresar el nuevo proyecto? Si o no: ", "Ingrese una respuesta valida: "):
            lista_proyectos.append(proyecto)
            print('SE DIO DE ALTA CORRECTAMENTE')
        else:
            decrementar_id()
            print("SE CANCELO EL INGRESO")
    else:
        bandera = False

    return bandera

#Funcion para mostrar un diccionario en particular
def mostrar_proyecto(proyecto:dict, informacion):
    for clave in proyecto:            
        informacion += str(proyecto[clave]) + " | "  
    print(informacion)

#Funcion para buscar un proyecto
def buscar_proyecto(lista_proyectos:list, dato_a_buscar:any, clave_buscada:str):
    retorno = 0
    for i in range(len(lista_proyectos)):
        if lista_proyectos[i][clave_buscada] == dato_a_buscar:
            print("Se encontro el proyecto")
            proyecto_aux = (lista_proyectos[i])
            mostrar_proyecto (proyecto_aux, "")
            retorno = i
            break
    return retorno


#Funcion para mostrar lista de diccionarios con el encabezado correspondiente
def mostrar_proyectos(lista_proyectos:list,):
    print ("PROYECTO\nID | NOMBRE DEL PROYECTO| DESCRIPCION | FECHA DE INICIO | FECHA DE FIN | PRESUPUESTO | ESTADO |\n")
    for proyecto in lista_proyectos:
        mostrar_proyecto(proyecto,"")


#Funcion para buscar proyecto por nombre
def buscar_proyecto_por_nombre(lista_proyectos: list):
    nombre_proyecto = input("Ingrese el nombre del proyecto que desea buscar: ")
    proyectos_encontrados = None
    for proyecto in lista_proyectos:
        if proyecto['Nombre del Proyecto'] == nombre_proyecto:
            proyectos_encontrados = proyecto
            mostrar_proyecto(proyectos_encontrados, "")
    return proyectos_encontrados
    


#Funcion para calcular promedio de presupuestos
def calcular_promedio_presupuesto(lista_proyectos:list):
    acumulador_presupuesto = 0
    contador_presupuesto = 0

    for proyecto in lista_proyectos:
        for clave, valor in proyecto.items():    #recorro y comparo los pares clave-valor
            if clave == 'Presupuesto':
                acumulador_presupuesto += valor
                contador_presupuesto += 1

    if contador_presupuesto == 0:
        print("NO SE ENCONTRARON PROYECTOS CON PRESUPUESTO.")
        return 0
    else:
        promedio_presupuestos = acumulador_presupuesto / contador_presupuesto
        print(f'EL PROMEDIO TOTAL DE LOS PRESUPUESTOS EXISTENTES ES DE: {promedio_presupuestos}')
        return promedio_presupuestos
    
#Funcion para modificar proyecto
def modificar_proyecto(lista_proyectos):
    id_proyecto = input("Ingrese el ID del proyecto que desea modificar: ")

    if not lista_proyectos:
        print("La lista de proyectos está vacía.")
        return
    
    proyecto_a_modificar = None
    
    for proyecto in lista_proyectos:
        if proyecto.get('id') == id_proyecto:
            proyecto_a_modificar = proyecto
            break

    if proyecto_a_modificar:
        print("Proyecto encontrado:")
        mostrar_proyecto(proyecto_a_modificar, "")
        print("¿Qué dato desea modificar?")
        print("1. Nombre del Proyecto")
        print("2. Descripción")
        print("3. Fecha de inicio")
        print("4. Fecha de fin")
        print("5. Presupuesto")
        print("6. Estado")
        opcion = input("Ingrese el número de la opción que desea modificar: ")
        if opcion == '1':
            nuevo_nombre = validar_nombre_proyecto("Ingrese el nuevo nombre del proyecto: ", "Ingrese un nombre correcto: ")
            proyecto_a_modificar['Nombre del Proyecto'] = nuevo_nombre
        elif opcion == '2':
            nueva_descripcion = validar_descripcion_proyecto("Ingrese la nueva descripcion del nuevo proyecto: ", "Ingrese una descripcion correcta: ")
            proyecto_a_modificar['Descripción'] = nueva_descripcion
        elif opcion == '3':
            nueva_fecha_inicio = validar_fechas("Ingrese la nueva fecha de inicio del proyecto: ", "Ingrese una fecha valida: ")
            proyecto_a_modificar['Fecha de inicio'] = nueva_fecha_inicio
        elif opcion == '4':
            nueva_fecha_fin = validar_fechas("Ingrese la nueva fecha de fin del proyecto: ", "Ingrese una fecha valida: ")
            proyecto_a_modificar['Fecha de Fin'] = nueva_fecha_fin
        elif opcion == '5':
            nuevo_presupuesto = validar_presupuesto_proyecto("Ingrese el nuevo presupuesto del proyecto: ", "Ingrese un presupuesto correcto: ")
            proyecto_a_modificar['Presupuesto'] = int(nuevo_presupuesto)
        elif opcion == '6':
            nuevo_estado = validar_estado("Ingrese el nuevo estado del proyecto: ", "Ingrese un estado correcto: ")
            proyecto_a_modificar["Estado"] = nuevo_estado
        else:
            print("Opción inválida.")
    else:
        print("No se encontró ningún proyecto con ese ID.")
    
    if proyecto_a_modificar:
        mostrar_proyecto(proyecto_a_modificar, "")


#Funcion para modificar el estado del proyecto
def modificar_estado(lista_proyectos):
    id_proyecto = input('Ingrese el ID del proyecto a modificar: ')
    #proyecto_a_modificar = buscar_proyecto(lista_proyectos, id_proyecto, 'id')
    proyecto_a_modificar = None

    for proyecto in lista_proyectos:
        if proyecto.get('id') == id_proyecto:
            proyecto_a_modificar = proyecto
            break

    if proyecto_a_modificar:
        nuevo_estado = 'Cancelado'
        proyecto_a_modificar['Estado'] = nuevo_estado
        print("Estado del proyecto modificado exitosamente.")
        mostrar_proyecto(proyecto_a_modificar, "")
    else:
        print("No se encontró ningún proyecto con ese ID.")
    
    return proyecto_a_modificar

#Funcion para cambiar el estado de aquellos proyectos cuya fecha de finalizacion sea anterior a la fecha actual ingresada

def comprobar_proyectos(lista_proyectos):
    fecha_actual = date.today()
    print(f"La fecha actual es: {fecha_actual.strftime('%d-%m-%Y')}")

    for proyecto in lista_proyectos:
        fecha_fin_proyecto = proyecto.get('Fecha de Fin', None)
        if fecha_fin_proyecto:
            try:
                fecha_fin_proyecto = datetime.strptime(fecha_fin_proyecto, "%d-%m-%Y").date()
                if fecha_fin_proyecto < fecha_actual:
                    proyecto['Estado'] = 'Finalizado'
                    mostrar_proyecto(proyecto, "")
            except ValueError:
                print("Formato de fecha incorrecto para el proyecto con ID:", proyecto.get('id', 'Desconocido'))

#Funcion para generar archivo csv con la lista actualizada
def generar_csv(nombre_archivo:str,lista:list):
    if len(lista) > 0:
        lista_claves = list(lista[0].keys())
        separador = ","
        cabecera = separador.join(lista_claves)
        print(cabecera)
        
        with open(nombre_archivo,"w") as archivo:
            archivo.write(cabecera + "\n")
            for elemento in lista:
                lista_valores = list(elemento.values())
                for i in range(len(lista_valores)):
                    lista_valores[i] = str(lista_valores[i])

                dato = separador.join(lista_valores)
                dato += "\n"
                archivo.write(dato)
    else:
        print("ERROR LISTA VACIA")

#Funcion para generar una lista con todos los proyectos FINALIZADOS que genera un archivo json
def generar_json_finalizados(lista_proyectos, nombre_archivo:str):
    proyectos_finalizados = []
    
    for proyecto in lista_proyectos:
        if proyecto['Estado'] == 'Finalizado':
            proyectos_finalizados.append(proyecto)
    
    if proyectos_finalizados:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(proyectos_finalizados, archivo, indent=4)
        print(f"Se han guardado {len(proyectos_finalizados)} proyectos finalizados en '{nombre_archivo}'.")
    else:
        print("No hay proyectos finalizados para guardar en el archivo JSON.")

#Funcion que genera la fecha actual
def obtener_fecha_actual():
    return datetime.now().strftime("%d-%m-%Y")

#Funcion para genera un reporte de presupuesto mayores al ingresado por consola
numero_reporte_presupuesto = 1 #Variable global
def generar_reporte_presupuesto(lista_proyectos):
    global numero_reporte_presupuesto  # Indicar que estamos usando la variable global

    # Solicitar al usuario que ingrese el presupuesto límite
    presupuesto_limite = int(input("Ingrese el presupuesto límite: "))

    # Obtener la fecha actual
    fecha_solicitud = obtener_fecha_actual()

    presupuestos_mayores = []

    for proyecto in lista_proyectos:
        if proyecto['Presupuesto'] > presupuesto_limite:
            presupuestos_mayores.append(proyecto)
    
    if presupuestos_mayores:
            cantidad_presupuestos_mayores = len(presupuestos_mayores)
        
            nombre_archivo = f'reporte_de_Presupuesto{numero_reporte_presupuesto}.txt'
            with open(nombre_archivo, 'w') as archivo:
                archivo.write(f"Reporte #{numero_reporte_presupuesto}\n")
                archivo.write(f"Fecha de solicitud: {fecha_solicitud}\n")
                archivo.write(f"Cantidad de proyectos que superan el presupuesto: {cantidad_presupuestos_mayores}\n\n")
                archivo.write("Listado de proyectos que superan el presupuesto:\n")
                for proyecto in presupuestos_mayores:
                    archivo.write(f"ID: {proyecto['id']}, Nombre: {proyecto['Nombre del Proyecto']}, Presupuesto: {proyecto['Presupuesto']}\n")
                
            print(f"SE HA GENERADO EL REPORTE NUMERO #{numero_reporte_presupuesto} CON EXITO. SE HAN ENCONTRADO {cantidad_presupuestos_mayores} PROYECTOS QUE SUPERAN EL PRESUPUESTO.")
            
            # Incrementar el número de reporte para el siguiente
            numero_reporte_presupuesto += 1
    else:
        print("NO SE ENCONTRARON PROYECTOS QUE SUPEREN EL PRESUPUESTO.")

#Funcion para ordenar de forma ascendente/descendente por Nombre de proyecto y Presupuesto
def ordenar_asc_desc_proyectos(lista):
    clave = input('Ingrese la clave sobre la cual desea que se realice el ordenamiento: ')
    orden_str = input('Ingrese que tipo de ordenamiento desea (ascendente/descendente): ')
    
        # Mapea la entrada del usuario a un booleano
    if orden_str.lower() == 'ascendente':
        orden = True
    elif orden_str.lower() == 'descendente':
        orden = False
    else:
        print("Error: Ingrese 'ascendente' o 'descendente' para el orden.")
        return None
    contador_cambios = 0
    if orden == True:
        for i in range(len(lista)):
            for j in range(i + 1,len(lista)):
                if lista[i][clave] > lista[j][clave]:
                    aux = lista[i] #Intercambio
                    lista[i] = lista[j] #Intercambio
                    lista[j] = aux #Intercambio
                    contador_cambios +=1
    else:
        for i in range(len(lista)):
            for j in range(i + 1,len(lista)):
                if lista[i][clave] < lista[j][clave]:
                    aux = lista[i] #Intercambio
                    lista[i] = lista[j] #Intercambio
                    lista[j] = aux #Intercambio
                    contador_cambios +=1
    return  lista


#Funcion para pasar fechas a formato datetime
def convertir_fecha(fecha):
    # Verificar si ya es un objeto datetime.datetime
    if isinstance(fecha, datetime):
        return fecha
    # Convertir cadena de texto a objeto datetime.date
    fecha_convertida = datetime.strptime(fecha, '%d-%m-%Y').date()
    return fecha_convertida

def ordenar_proyectos_por_fecha(lista):
    orden_str = input('Ingrese que tipo de ordenamiento desea (ascendente/descendente): ')
    clave = 'Fecha de inicio'
    for proyecto in lista:
        proyecto['Fecha de inicio'] = convertir_fecha(proyecto['Fecha de inicio'])

    if orden_str.lower() == 'ascendente':
        orden = True
    elif orden_str.lower() == 'descendente':
        orden = False
    else:
        print("Error: Ingrese 'ascendente' o 'descendente' para el orden.")
        return None
    contador_cambios = 0
    n = len(lista)

    if orden:
        for i in range(n):
            for j in range(0, n-i-1):
                if lista[j][clave] > lista[j+1][clave]:
                    lista[j], lista[j+1] = lista[j+1], lista[j]
                    contador_cambios += 1
    else:
        for i in range(n):
            for j in range(0, n-i-1):
                if lista[j][clave] < lista[j+1][clave]:
                    lista[j], lista[j+1] = lista[j+1], lista[j]
                    contador_cambios += 1

    for proyecto in lista:
        proyecto['Fecha de inicio'] = proyecto['Fecha de inicio'].strftime('%d-%m-%Y')

#FUNCION PARA RETOMAR PROYECTO
def retomar_proyecto(lista_proyectos):
    mostrar_proyectos(lista_proyectos)
    proyecto_id = input("Ingrese el ID del proyecto que desea retomar: ")

    for proyecto in lista_proyectos:
        if str(proyecto["id"]) == proyecto_id:  # Convertir el ID del proyecto a cadena para la comparación
            if proyecto["Estado"].lower() == "cancelado":
                if validar_proyecto_para_retomar(proyecto):
                    proyecto["Estado"] = "Activo"
                    print(f"El proyecto con ID {proyecto_id} ha sido retomado y está ahora en estado 'Activo'.")
                else:
                    print(f"El proyecto con ID {proyecto_id} no cumple con los requisitos para ser retomado.")
            else:
                print(f"El proyecto con ID {proyecto_id} no está cancelado y no puede ser retomado.")
            return

    print(f"No se encontró un proyecto con el ID {proyecto_id}.")


#FUNCION PARA VALIDAR LA INFORMACION YA INGRESADA DE UN PROYECTO Y VER SI LO PUEDO RETORNAR
def validar_proyecto_para_retomar(proyecto):
    # Verifica que el nombre del proyecto no esté vacío
    if not proyecto.get("Nombre del Proyecto"):
        print(f"El proyecto con ID {proyecto['id']} no tiene un nombre válido.")
        return False

    # Verifica que la descripción no esté vacía
    if not proyecto.get("Descripción"):
        print(f"El proyecto con ID {proyecto['id']} no tiene una descripción válida.")
        return False

    # Verifica que las fechas de inicio y fin sean válidas
    if not proyecto.get("Fecha de inicio") or not proyecto.get("Fecha de Fin"):
        print(f"El proyecto con ID {proyecto['id']} no tiene fechas válidas.")
        return False

    try:
        fecha_inicio = datetime.strptime(proyecto["Fecha de inicio"], "%d-%m-%Y").date()
        fecha_fin = datetime.strptime(proyecto["Fecha de Fin"], "%d-%m-%Y").date()
        if fecha_inicio > fecha_fin:
            print(f"El proyecto con ID {proyecto['id']} tiene una fecha de inicio posterior a la fecha de fin.")
            return False
    except ValueError:
        print(f"El proyecto con ID {proyecto['id']} tiene un formato de fecha incorrecto.")
        return False

    # Verifica que el presupuesto sea un número positivo
    try:
        presupuesto = float(proyecto.get("Presupuesto", 0))
        if presupuesto <= 0:
            print(f"El proyecto con ID {proyecto['id']} no tiene un presupuesto válido.")
            return False
    except ValueError:
        print(f"El proyecto con ID {proyecto['id']} tiene un formato de presupuesto incorrecto.")
        return False

    return True




#Funcion para genera un reporte de; Proyecto ingresado por consola
numero_reporte_proyecto = 1 #Variable global
def generar_reporte_nombre(lista_proyectos):
    global numero_reporte_proyecto  # Indicar que estamos usando la variable global

    # Solicitar al usuario que ingrese el presupuesto límite
    nombre_proyecto = input("Ingrese el Nombre del proyecto requerido: ")

    # Obtener la fecha actual
    fecha_solicitud = obtener_fecha_actual()

    proyecto_requerido = []

    for proyecto in lista_proyectos:
        if proyecto['Nombre del Proyecto'] == nombre_proyecto:
            proyecto_requerido.append(proyecto)
    
    if proyecto_requerido:
            cantidad_proyectos_requeridos = len(proyecto_requerido)
        
            nombre_archivo = f'reporte_de_Proyecto_{numero_reporte_proyecto}.txt'
            with open(nombre_archivo, 'w') as archivo:
                archivo.write(f"Reporte #{numero_reporte_proyecto}\n")
                archivo.write(f"Fecha de solicitud: {fecha_solicitud}\n")
                archivo.write(f"Cantidad de proyectos: {cantidad_proyectos_requeridos}\n\n")
                archivo.write("Listado de datos del proyecto:\n")
                for proyecto in proyecto_requerido:
                    archivo.write(f"ID: {proyecto['id']}, Nombre: {proyecto['Nombre del Proyecto']}\n Descripcion: {proyecto['Descripción']}, Fecha de inicio: {proyecto['Fecha de inicio']}, Fecha de Fin: {proyecto['Fecha de Fin']}, Presupuesto: {proyecto['Presupuesto']}, Estado: {proyecto['Estado']}\n")
                
            print(f"Se ha generado el reporte #{numero_reporte_proyecto} con éxito. Se ha encontrado {cantidad_proyectos_requeridos} proyectos.")
            
            # Incrementar el número de reporte para el siguiente
            numero_reporte_proyecto += 1
    else:
        print("No se encontraron proyectos con el nombre ingresado.")


#Funcion para calcular promedio presupuestos cancelados segun descripcion
def  promedio_presupuesto_cancelados_desarrollo(lista):
    presupuesto_total = 0
    contador_proyectos = 0
    promedio_total = 0

    for proyecto in lista:
        #Voy a iterar en la lista y a preguntar proyecto por proyecto si su estado es cancelado
        # y si la palabra 'Desarrollo' esta presente en el valor de la clave Descripcion
        if proyecto['Estado'] == 'Cancelado' and 'Desarrollo' in proyecto['Descripción']:
            presupuesto_total += proyecto['Presupuesto']
            contador_proyectos += 1

            if contador_proyectos == 0:
                print('Error: No existen proyectos con los criterios solicitados')
                return None
            
    promedio_total = presupuesto_total / contador_proyectos
    print(f'El promedio total de los proyectos cancelados que incluyen la palabra desarrollo es de: {promedio_total}')


#Funcion para obtener los 3 presupuestos mas bajos de los proyectos finalizados
def menor_presupuesto_finalizados(lista, clave):
    proyectos_finalizados = []
    
    #Primero recorro la lista de proyectos para encontrar aquellos finalizados y separarlos
    for proyecto in lista:
        if proyecto['Estado'] == 'Finalizado':
            proyectos_finalizados.append(proyecto)
    
    #segundo recorro la lista de proyectos_finalizados para ordenarlos de forma ascendente
    for i in range(len(proyectos_finalizados)):
            for j in range(i + 1,len(proyectos_finalizados)):
                if proyectos_finalizados[i][clave] > proyectos_finalizados[j][clave]:
                    aux = proyectos_finalizados[i] #Intercambio
                    proyectos_finalizados[i] = proyectos_finalizados[j] #Intercambio
                    proyectos_finalizados[j] = aux #Intercambio
                    
    #Chequeo si la cantidad de proyectos dentro de la lista es la que necesito
    if len(proyectos_finalizados) < 3:
        print('Error: la cantidad de proyectos finalizados no es suficiente')
    else:
        primer_finalizado = proyectos_finalizados[0]
        segundo_finalizado = proyectos_finalizados[1]
        tercer_finalizado = proyectos_finalizados[2]
    
        mostrar_proyecto(primer_finalizado, "Primer puesto: ")
        mostrar_proyecto(segundo_finalizado, "Segundo puesto: ")
        mostrar_proyecto(tercer_finalizado, "Tercer puesto: ")

#Funcion generar archivo actualizado
def actualizar_csv(lista_proyectos, nombre_archivo):
    # Abrir el archivo CSV en modo escritura
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
        
        # Defino los nombres de las columnas buscando en el primer diccionario todas las claves.
        columnas = lista_proyectos[0].keys()
        
        # Creo el escritor CSV con DicWriter que me permite escribir diccionarios
        escritor_csv = csv.DictWriter(archivo, fieldnames=columnas)
        
        escritor_csv.writeheader()  #writeheader() crea el encabezado
        
        #Itero y escribo los datos de cada proyecto en el archivo CSV
        for proyecto in lista_proyectos:
            escritor_csv.writerow(proyecto)
    
    print(f"El archivo {nombre_archivo} se ha actualizado correctamente.")

