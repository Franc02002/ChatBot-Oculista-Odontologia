#En este archivo estaran las preguntas que realiza y las respuestas a las acciones 

from datetime import datetime
import pandas as pd
import random

def sacarTurno(opcion,planilla):
    #Verifica con quien quiere sacar turno y consulta fecha;hora para luego entregar los datos al metodo buscarTurno
    seguir= True
    if opcion==1:
        profesional="Odontologo"
    else:
        profesional="Oculista"

    print("Ha seleccionado pedir un turno con un " + profesional + " ,Horario de Atencion Lunes a Viernes de 9HS a 17HS")
    while(seguir):
        dia=input("Indique que dia de esta semana necesita el turno *SUPONGA QUE ES LUNES* u escriba 'SALIR' para volver al menu principal" "\n")
        if dia.lower()=="salir":
            seguir= False
        else:
            dia =dia.capitalize()
            hora= input("Indique la hora en la que necesita el turno, ej: 15:00" "\n")
            if verificaHora(hora) and dia in {"Lunes","Martes","Miercoles","Jueves","Viernes"} :         
                 seguir= buscarTurno(dia,hora, planilla)           
            else:
                print("Fecha u Hora ingresada incorrecta o con formato incorrecto, por favor vuelva a ingresarla" "\n")       

def verificaHora(hora_texto):
    #verifica si la fecha y hora estan en formato correcto, uso try para capturar el posible error
    try:         
        datetime.strptime(hora_texto,"%H:%M")
        return True
        
    except ValueError:
        return False


def buscarTurno(dia,hora,planilla):
    #Busco dentro de los turnos disponibles si se encuentra disponible el pedido y lo confirma, en caso de no estarlo ofrece variantes en el mismo dia
    
    filtro1= planilla["Dia"] == dia
    filtro2= planilla["Hora"] == hora
    indiceBuscado=int(planilla[filtro1 & filtro2].index[0])
    
    if pd.isna(planilla.at[indiceBuscado,"DNI"]): #Si la celda en la col DNI esta vacia es porque el dia y horario que solicito esta desocupado
        dniAsociado=input("El dia y hora elegido estan disponibles, por favor ingrese su DNI u escriba 'salir' para volver" "\n") #PULIR PARA CUANDO 1 PERSONA TENGA MAS DE UN TURNO EN LA MISMA SEMANA
        if dniAsociado.lower() == "salir":
            return True #Para indicarle al metodo que invocó a este que aun continua la ejecucion de sacar un turno.
        while(True):
            if verificaDni(dniAsociado):            
                return asignaTurno(dia,hora,dniAsociado,planilla,indiceBuscado)     
            else:
                dniAsociado= input("El DNI ingresado no tiene formato valido, por favor vuelva a ingresarlo" "\n")   
      
    else: #Entra a este else cuando el dia y horario elegido en un principio esta ocupado
        print("Lamentablemente no hay turno disponible para el horario que necesita, a continuacion vera los turnos disponibles correspondiente al dia " + dia)
        dfFiltrado= obtieneHorariosDeUnDia(dia,planilla) #Espera un DF que solo tiene Dia==dia y DNI vacio, de esta manera puedo buscar que horarios de "dia" estan libres
        horariosDisponibles= dfFiltrado.loc[:,"Hora"]
        while(True):
            print(horariosDisponibles.tolist())
            horarioElegido = input("\n¿Cuál deseas elegir? U escriba 'salir' para volver atras: " "\n")
            if horarioElegido.lower()== 'salir':
                return True
            if horarioElegido in horariosDisponibles.tolist():
                while(True):
                    dniAsociado= input("Indique su DNI para terminar la confirmacion" "\n")
                    if verificaDni(dniAsociado):
                        asignaTurno(dia,horarioElegido,dniAsociado,planilla,int((horariosDisponibles[horariosDisponibles == horarioElegido]).index[0]))
                        return False
                    else:
                          print("El DNI ingresado no tiene formato valido, por favor vuelva a ingresarlo")           
            else:
                print("El horario elegido es incorrecto ,por favor vuelva a intentarlo")

 
def verificaDni(dni):
    #Verifica si el numero ingresado coincide con el formato de un DNI
    dniLimpio = dni.strip() #strip() es como trim en java, limpia espacios    
    try:
        dni_numero = int(dniLimpio)
        if 7000000 <= dni_numero <= 99999999:
            return True
        else:
            return False
            
    except ValueError:
        #Si fallo la conversion a INT o el numero no esta entre los digitos dados, retorno False
        return False       
    
def asignaTurno(dia,hora,dni,planilla,indice):
    #Metodo encargado de asigna el turno en la planilla, previamente se hicieron las verificaciones necesarias
    nombre= input("Por favor indique Nombre" "\n")
    apellido= input("Por favor indique su Apellido" "\n")
    planilla.at[indice,"DNI"]= int(dni)
    planilla.at[indice,"Nombre_Apellido"]= nombre+ " " +apellido
    print("El turno ha sido confirmado con exito, lo esperamos el dia: " + dia + "  " + hora + "Hs con su DNI")
       


def obtieneHorariosDeUnDia(dia,planilla):
    #Metodo que devuelve una lista con los horarios libres en el dia previamente elegido
    filtroHorario= planilla["Dia"] == dia 
    filtroDesocupado= planilla["DNI"].isna()   
    indicesHorarioDesocupado= planilla[filtroHorario & filtroDesocupado]
    return indicesHorarioDesocupado
    
    
    
def cancelarTurno(dni,planilla):
    #Este metodo busca el/los turnos ligados al DNI, si es solo uno elimina y da la notificacion a la persona en otro caso le muestra una lista de los turnos que tiene y esta elige cual cancelar
    filtro1= (planilla["DNI"] == dni)
    indicesDniCoincidentes = filtro1[filtro1].index.tolist()
    if indicesDniCoincidentes:
        if len(indicesDniCoincidentes)>1:
            dfDiayHorariosCoincidentes= obtieneDiasyHorario(indicesDniCoincidentes,planilla)
            print("El Dni ingresado tiene mas de un turno asociado, a continuacion vera los turnos y debera indicar cual desea cancelar" "\n")
            opciones= []
            for indice,fila in dfDiayHorariosCoincidentes.iterrows():
                dia= str(fila["Dia"]).strip()
                hora= str(fila["Hora"]).strip()

                print(f"{dia} a las {hora}hs")
                opciones.append(f"{dia} {hora}")
        
            while(True):
                eleccion= input("Escriba el dia y hora que desea. Ej: lunes 09:30" "\n").strip()       
                if eleccion in opciones:
                    #falta hacer la logica para ingresar en la planilla los cambios
                    a=a
                else:
                    print("La opcion elegida no es correcta, vuelva a ingresar los datos")
            
        else:
            indice=int(indicesDniCoincidentes[0])
            planilla.at[indice, "DNI"]= pd.NA
            planilla.at[indice,"Nombre_Apellido"]= pd.NA
            print("El turno ha sido cancelado con exito" "\n")
        
    else: 
        respuesta=input("No existen turnos asociados al Dni ingresado, vuelva a ingresar el Dni o escriba 'salir' para volver al menu principal")    
        
        
def limpiaFormatoTexto(texto):
    # 1. Pasamos todo a minúscula obligatoriamente
    texto_limpio = str(texto).lower()
    
    # 2. Matamos las tildes a lo bruto
    texto_limpio = texto_limpio.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    
    # 3. EL GOLPE FINAL: split() rompe por CUALQUIER tipo de espacio raro, 
    # y join() lo pega de nuevo sin espacios en el medio.
    texto_blindado = "".join(texto_limpio.split())
    
    return texto_blindado      
    

            

def obtieneDiasyHorario(listaIndices,planilla):
    #Este metodo recibe una lista de indices y devuelve un DF con los dias y horarios que corresponden a los indices
    dfFiltrado= planilla.loc[listaIndices,["Dia", "Hora"]]
    return dfFiltrado
    
        


def main():
    planillaTurnosOculista= pd.read_excel(r"ChatBot-Oculista-Odontologia\BD\PlanillaOculista.xlsx")
    planillaTurnosOdontologo= pd.read_excel(r"ChatBot-Oculista-Odontologia\BD\PlanillaOdontologo.xlsx")
    #Convierto los datos en string para que no se rompa al comparar con la hora pasada por parametro, esto porque Pandas usa Datetime
    planillaTurnosOculista["Hora"] = planillaTurnosOculista["Hora"].astype(str).str.strip().str[:5]
    planillaTurnosOculista["Dia"] = planillaTurnosOculista["Dia"].astype(str).str.strip()
    planillaTurnosOdontologo["Hora"] = planillaTurnosOdontologo["Hora"].astype(str).str.strip().str[:5]
    planillaTurnosOdontologo["Dia"] = planillaTurnosOdontologo["Dia"].astype(str).str.strip()
    seguir=True
    print("Hola soy A.V.I, el asistente de SAMServices")
    while(seguir):
        print("Indique el numero correspondiente a lo que desea realizar")
        opcion=int(input("1-Solicitar turno con Odoltologo" "\n" "2-Solicitar turno con Oculista" "\n" "3-Dar de baja un turno" "\n" "4-Terminar la consulta" "\n"))
        if opcion==1:
            #Utilizo NOT de manera que se vea mas logico que false es para no continuar con el while y true es para continuarlo
            seguir= not sacarTurno(opcion,planillaTurnosOdontologo)         

        elif opcion==2:
            seguir= sacarTurno(opcion,planillaTurnosOculista)

        elif opcion==3 :
                continua=True
                while(continua): 
                    respuesta=int(input("1-Cancelar turno con Odontologo" "\n" "2-Cancelar turno con Oculista" "\n" "3-Salir" "\n" "Coloque el numero que corresponde a lo que desea realizar" "\n"))
                    if respuesta in {1,2,3}:
                        if respuesta==3:
                            continua=False
                        else:        
                            terminar=True
                            while(terminar):
                                dni= input("Por favor indique su DNI u escriba 'salir' para volver atras" "\n" )
                                if dni.lower() == "salir":
                                    terminar=False
                                else: 
                                    if verificaDni(dni):
                                        dni= int(dni)
                                        if respuesta==2:
                                            terminar=cancelarTurno(dni,planillaTurnosOculista)
                                        else:
                                            terminar=cancelarTurno(dni,planillaTurnosOdontologo)    
                                    else:
                                        print("EL DNI ingresado tiene un formato invalido, por favor vuelva a ingresarlo")
                    else:
                        print("Respuesta incorrecta, elija una correcta" "\n")            
                
        else:
            print("La opcion elegida es incorrecta, por favor vuelva a intentarlo")
    
    print("Sesion Finalizada")     


if __name__ == "__main__":
    main()

    #PODRIA REALIZARSE UNA VERIFICACION INDIVIDUAL PARA VER SI LA HORA O LA FECHA FUE INGRESADO DE MANERA INCORRECTA, AHORA ESTA DISENIADO PARA QUE REPITA AMBAS AUNQUE SOLO UNA ESTE MAL