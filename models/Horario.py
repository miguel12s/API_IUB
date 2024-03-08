from datetime import datetime
from datetime import timedelta
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from schemas.Horario import Horario
from schemas.PeticionAceptada import PeticionAceptada
from schemas.Solicitud import Solicitud
from models.docente import ModelDocente

import mysql

class SchedulerCalendar:

    def mostrarSolicitudHorario(user_id):
         try:
            conn=get_db_connection()
            cursor=conn.cursor()
            cursor.execute("""

SELECT u2.nombres,u2.apellidos,u.foto,ph.tema,date_format(ph.hora_inicial,'%H:%i'),date_format(ph.hora_final,'%H:%i'),ph.fecha,s.salon,te.estado FROM peticiones_horario ph join usuarios u on u.id_usuario=ph.id_estudiante
join usuarios u2 on ph.id_docente=u2.id_usuario
join salones s on s.id_salon=ph.id_salon
join tipoxestado te on te.id_tipoxestado=ph.id_estado where u.id_usuario=%s
""",(user_id,))
            data=cursor.fetchall()
            payload=[]
            res={}
            for i in data:
                 res={
                      'nombres':i[0],
                      'apellidos':i[1],
                      'foto':i[2],
                      'tema':i[3],
                      'hora_inicial':i[4],
                      'hora_final':i[5],
                      'fecha':i[6],
                      'salon':i[7],
                      'estado':i[8]
                 }
                 payload.append(res)
                 res={}
            json_data=jsonable_encoder(payload)
            if json_data:
                 print(json_data)
                 return json_data
            return {"error":"no existe ninguna solicitud"}
         except Exception as e:
              return HTTPException(status_code=500,detail=e)
    def getHorarioForIdEstudiante(id):
            conn=get_db_connection()
            cursor=conn.cursor()
            cursor.execute("""     SELECT ht.id_tutoria,f.facultad,p.programa,m.materia ,s.salon,ht.id_usuario,txe.estado,ht.cupos,ht.tema,ht.fecha, date_format(ht.hora_inicial,'%H:%i') as hora_inicial,date_format(ht.hora_final,'%H:%i') as hora_final  FROM `horario_tutorias` ht 
join salones s on ht.id_salon=s.id_salon
join tipoxestado txe on ht.id_estado_tutoria=txe.id_tipoxestado 
join fpxmateria fpxm on fpxm.id_fpxm=ht.id_fpxm
join facultadxprograma fxp on fxp.id_fxp=fpxm.id_fxp
join facultades f on f.id_facultad=fxp.id_facultad
join programas p on p.id_programa=fxp.id_programa
join materias m on m.id_materia=fpxm.id_materia
where txe.id_tipoxestado=6 and id_usuario=%s;""",(id,))
            data=cursor.fetchall()
            payload=[]
            content={}
            for result in data:
                   content = {
                       'id':result[0],
                       'facultad':result[1],
                       'programa':result[2],
                       'materia':result[3],
                       'salon':result[4],
                       'id_usuario':result[5],
                       'estado_tutoria':result[6],
                       'cupos':result[7],
                       'tema':result[8],
                       'fecha':result[9],
                       'hora_inicial':result[10],
                       'hora_final':result[11]
                    

                }
                   payload.append(content)
                   
                   content={}
            json_data=jsonable_encoder(payload)
            print(payload)
            if json_data:
                return {"resultado":json_data} 
            return {"error":"no existe ningun horario creado"}
    def getSchedulerCalendar(id_usuario):
          try:
            conn=get_db_connection()
            cursor=conn.cursor()
            cursor.execute("""SELECT ht.id_tutoria,f.facultad,p.programa,m.materia ,s.salon,le.id_usuario,txe.estado,ht.cupos,ht.tema,ht.fecha,ht.hora_inicial,ht.hora_final,u.nombres,u.apellidos  FROM `horario_tutorias` ht 
join lista_estudiantes le on le.id_tutoria=ht.id_tutoria
join salones s on ht.id_salon=s.id_salon
join tipoxestado txe on ht.id_estado_tutoria=txe.id_tipoxestado 
join fpxmateria fpxm on fpxm.id_fpxm=ht.id_fpxm
join facultadxprograma fxp on fxp.id_fxp=fpxm.id_fxp
join facultades f on f.id_facultad=fxp.id_facultad
join programas p on p.id_programa=fxp.id_programa
join materias m on m.id_materia=fpxm.id_materia
join usuarios u on u.id_usuario=ht.id_usuario
where txe.id_tipoxestado=6 and le.id_usuario=%s;""",(id_usuario,))
            data=cursor.fetchall()
            payload=[]
            content={}
            for result in data:
                start_datetime_str = f"{result[9]} {result[10]}"
                end_datetime_str = f"{result[9]} {result[11]}"

                    # Convertir las cadenas de fecha y hora a objetos datetime
                start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')
                end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S')
                

                content = {
                        'id':result[0],
                       'title':f"{result[8]} {result[10]} - {result[11]}",
                       'date':result[9],
                       'start':start_datetime,
                       'end':end_datetime

                    

                }
                payload.append(content)
                   
                content={}
            
            json_data=jsonable_encoder(payload)
            print(json_data)
            return json_data
          except Exception as e:
                print(e)
                return HTTPException(status_code=400,detail=e)
    def getSchedulerCalendarTeacher(id_usuario):
          try:
            conn=get_db_connection()
            cursor=conn.cursor()
            cursor.execute("""SELECT ht.id_tutoria,f.facultad,p.programa,m.materia ,s.salon,txe.estado,ht.cupos,ht.tema,ht.fecha,ht.hora_inicial,ht.hora_final,u.nombres,u.apellidos  FROM `horario_tutorias` ht 
join salones s on ht.id_salon=s.id_salon
join tipoxestado txe on ht.id_estado_tutoria=txe.id_tipoxestado 
join fpxmateria fpxm on fpxm.id_fpxm=ht.id_fpxm
join facultadxprograma fxp on fxp.id_fxp=fpxm.id_fxp
join facultades f on f.id_facultad=fxp.id_facultad
join programas p on p.id_programa=fxp.id_programa
join materias m on m.id_materia=fpxm.id_materia
join usuarios u on u.id_usuario=ht.id_usuario
where txe.id_tipoxestado=6 and ht.id_usuario=%s;""",(id_usuario,))
            data=cursor.fetchall()
            payload=[]
            content={}
            for result in data:
                start_datetime_str = f"{result[8]} {result[9]}"
                end_datetime_str = f"{result[8]} {result[10]}"

                    # Convertir las cadenas de fecha y hora a objetos datetime
                start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')
                end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S')
                

                content = {
                        'id':result[0],
                       'title':f"{result[7]} {result[9]} - {result[10]}",
                       'date':result[9],
                       'start':start_datetime,
                       'end':end_datetime

                    

                }
                payload.append(content)
                   
                content={}
            
            json_data=jsonable_encoder(payload)
            print(json_data)
            return json_data
          except Exception as e:
                print(e)
                return HTTPException(status_code=400,detail=e)
    def createNotificacionHorario(solicitud:Solicitud,id_user):
        try:

            conn = get_db_connection()
            cursor = conn.cursor()
            id_fpxm=getidfpxm(solicitud)
            cursor.execute("""
insert into peticiones_horario ( id_docente, id_estudiante, id_salon, tema, fecha, hora_inicial, hora_final,id_fpxm) values (%s,%s,%s,%s,%s,%s,%s,%s)


""",(solicitud.id_docente,id_user,solicitud.id_salon,solicitud.tema,solicitud.fecha,solicitud.hora_inicial,solicitud.hora_final,id_fpxm))
            conn.commit()
            # ModelDocente.createHorarioForPeticion(solicitud,id_fpxm)
            
            return {"success":"la solicitud de la tutoria ha sido enviada"}
           
        except mysql.connector.Error as err:
            print(err)
            conn.rollback()
            return ({"error": "la solicitud no pudo ser enviada intente mas tarde"})
        finally:
            conn.close()
    def mostrarSolicitudes(id_docente):
        try:

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
SELECT concat(u.nombres,' ',u.apellidos) as nombre_estudiante ,pth.tema,date_format(pth.hora_final,'%H:%i'),date_format(pth.hora_inicial,'%H:%i'),s.salon ,pth.fecha,pth.id_peti_hora,pth.id_estado,txe.estado,pth.id_fpxm,c.id_capacidad FROM peticiones_horario pth 
join usuarios u on u.id_usuario=pth.id_estudiante
join salones s on s.id_salon=pth.id_salon
join capacidades c on c.id_capacidad=s.id_capacidad
join tipoxestado txe on txe.id_tipoxestado=pth.id_estado
where pth.id_docente=%s and pth.id_estado=23

""",(id_docente,))
            result=cursor.fetchall()
            solicitud={}
            payload=[]
            for soli in result:
                solicitud={
                     'nombre_estudiante':soli[0],
      'tema':soli[1] ,
      'hora_final':soli[2] ,
      'hora_inicial':soli[3] ,
      'salon': soli[4],
      'fecha':soli[5] ,
      'id_peti_hora':soli[6],
      'id_estado': soli[7],
      'estado': soli[8],
      'id_fpxm':soli[9],
      'id_capacidad':soli[10]
                }
                payload.append(solicitud)
                solicitud={}
            json_data=jsonable_encoder(payload)

            return {"success":json_data}
           
        except mysql.connector.Error as err:
            print(err)
            conn.rollback()
            return ({"error": "la solicitud no pudo ser enviada intente mas tarde"})
        finally:
            conn.close()
    def cambiarEstadoPeticion(id_peticion,id_user,id_estado):
        try:

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
UPDATE `peticiones_horario` ph set ph.id_estado=%s where ph.id_docente=%s and ph.id_peti_hora=%s

""",(id_estado,id_user,id_peticion))
            conn.commit()
            return {"success":"el estado de la tutoria ha sido actualizada"}
           
        except mysql.connector.Error as err:
            print(err)
            conn.rollback()
            return ({"error": "la solicitud no pudo ser enviada intente mas tarde"})
        finally:
            conn.close()

    def peticionAceptada(peticion:PeticionAceptada,id_usuario):
        try:
            existTutoria=ModelDocente.verify_hour(peticion.hora_inicial,peticion.hora_final,peticion.fecha,id_usuario)
            if(existTutoria==0):

                ModelDocente.createHorarioForPeticion( peticion,peticion.id_fpxm,id_usuario)
                SchedulerCalendar.cambiarEstadoPeticion(peticion.id_peti_hora,id_usuario,24)
                return {"success":"solicitud aceptada"}
            else:
                return {"error":"el horario ya existe"}
        except Exception as e:
            print(e)


def getidfpxm(solicitud:Solicitud):
    try:
         conn = get_db_connection()
         cursor = conn.cursor()
         cursor.execute("""
SELECT fpxm.id_fpxm FROM `fpxmateria` fpxm 
join facultadxprograma fxp on fxp.id_fxp=(select id_fxp from facultadxprograma fxp2 where fxp2.id_facultad=%s and fxp2.id_programa=%s) where fpxm.id_materia=%s

""",(solicitud.id_facultad,solicitud.id_programa,solicitud.id_materia))
         id_fpxm=cursor.fetchone()[0]
         return id_fpxm
    except:
        raise HTTPException(status_code=500)
    finally:
        conn.close()