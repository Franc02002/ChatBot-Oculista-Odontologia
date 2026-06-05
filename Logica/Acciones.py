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
                seguir= buscarTurno(dia,f"{hora}:00", planilla)           
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
    estadoTurno = planilla.at[hora,dia];
    if pd.isna(estadoTurno) or estadoTurno== "":
        dniAsociado=input("El dia y hora elegido estan disponibles, por favor ingrese su DNI para confirmar el turno u escriba 'salir' para volver" "\n") #PULIR PARA CUANDO 1 PERSONA TENGA MAS DE UN TURNO EN LA MISMA SEMANA
        if dniAsociado.lower() == "salir":
            return True #Para indicarle al metodo que invoco a este que aun continua la ejecucion de sacar un turno.
        elif verificaDni(dniAsociado):
            planilla.at[hora,dia]= int(dniAsociado)
            print("Su turno fue confirmado con exito, recuerde presentarse el dia: " + dia + hora + "hs con su DNI")
            return False
        
    else:
        print("Lamentablemente no hay turno disponible para el horario que necesita, a continuacion vera los turnos disponibles correspondiente al dia " + dia)
        horariosDiposnibles= obtieneHorariosDeUnDia(dia,planilla) #Espera una lista con los horarios disponibles en 'dia'
        while(True):
            horarioElegido = input(f"Horarios disponibles: {', '.join(horariosDiposnibles)}\n¿Cuál deseas elegir? U escriba 'salir' para volver atras: " "\n") #join arma una cadena con esa lista para luego mostrarla por pantalla y que la persona elija el horario que desea
            if horarioElegido.lower()== 'salir':
                return True
            if f"{horarioElegido}:00" in horariosDiposnibles:
                while(True):
                    dniAsociado= input("Indique su DNI para terminar la confirmacion" "\n")
                    if verificaDni(dniAsociado):
                        planilla.at[f"{horarioElegido}:00",dia]= int(dniAsociado)
                        print("La confirmacion fue realizada con exito, recuerde presentarse el dia: " + dia + "  " + horarioElegido + "Hs con su DNI")
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


def obtieneHorariosDeUnDia(dia,planilla):
    #Metodo que devuelve una lista con los horarios libres en el dia previamente elegido
    filtro= (planilla[dia].isna()) | (planilla[dia] == "")
    horariosLibres= planilla.index[filtro]
    return list(horariosLibres)

def cancelarTurno(dni,planilla):
    #Este metodo busca el/los turnos ligados al DNI, si es solo uno elimina y da la notificacion a la persona,
    #En caso de tener mas de un turno asociado, el metodo muestra por pantalla los turnos y el usuario elige cual dar de baja

    turnosCoincidentes= planilla.where(planilla == dni) #Obtengo una nueva planilla donde las celdas que no sean coincidentes con el DNI buscado estaran con valor 'null'
    listaTurnosCoincidentes= turnosCoincidentes.stack().dropna().index  #Paso a una lista las keys(hora,dia) de las casillas no nulas, de esta forma obtengo los turnos que estan asociados al DNI



def main():
    planillaTurnosOculista= pd.read_excel(r"F:\Programacion\ProyectosProgramacion\DiplomaturaUBA\ChatBot\BD\PlanillaOculista.xlsx",index_col=0)
    planillaTurnosOdontologo= pd.read_excel(r"F:\Programacion\ProyectosProgramacion\DiplomaturaUBA\ChatBot\BD\PlanillaOdontologo.xlsx",index_col=0)
    #Convierto los datos en string para que no se rompa al comparar con la hora pasada por parametro, esto porque Pandas usa Datetime
    planillaTurnosOdontologo.index = planillaTurnosOdontologo.index.astype(str)
    planillaTurnosOculista.index = planillaTurnosOdontologo.index.astype(str)
    seguir=True
    print("Hola soy A.V.I, el asistente de SAMServices")
    while(seguir):
        print("\n")
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
                    respuesta=int(input("1-Cancelar turno con Oculista" "\n" "2-Cancelar turno con Odontologo" "\n" "3-Salir" "\n" "Coloque el numero que corresponde a lo que desea realizar" "\n"))
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
                                        if respuesta==1:
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