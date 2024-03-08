from config.db_config import get_db_connection
from schemas.Horario import Horario
from schemas.PeticionAceptada import PeticionAceptada
from schemas.Solicitud import Solicitud

class ModelDocente():

    
    def verify_hour(horaInicio:str,horaFin:str,fecha:str,id_usuario:int):
        bd=get_db_connection()
        cursor=bd.cursor()
        # sql=f"""SELECT count(*) from horario_tutorias ht where ht.hora_inicial="{horaInicio}" and ht.hora_final="{horaFin}" and ht.fecha="{fecha}" and ht.id_usuario={id_usuario} """
        # print(sql)
        # cursor.execute(sql)
        sql="""SELECT count(*) from horario_tutorias where fecha=%s and hora_inicial<%s and hora_final>%s and id_usuario=%s """
        print(sql)
        cursor.execute(sql,(fecha,horaFin,horaInicio,id_usuario))
        existe=cursor.fetchone()[0]
        cursor.close()
        return existe
    def createHorarioForPeticion(solicitud:PeticionAceptada,id_fpxm:int,id_user:int):
        try:
            res=getIdForData(solicitud.salon)
            print(res)
            if(res['success']):
                bd=get_db_connection()
                cursor=bd.cursor()
                cursor.execute("""
                INSERT INTO horario_tutorias (id_fpxm, id_salon, id_usuario, id_estado_tutoria, cupos, tema, fecha, hora_inicial, hora_final)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(id_fpxm, res['success'],id_user,6,solicitud.id_capacidad,solicitud.tema,solicitud.fecha,solicitud.hora_inicial,solicitud.hora_final))
                bd.commit()
                cursor.close()
            else:
                print(res['error'])
        except Exception as e:
            print(e)

    def createHorario(horario:Horario,id_usuario:int,id_fpxm:int):
        bd=get_db_connection()
        cursor=bd.cursor()
        cursor.execute("""
        INSERT INTO horario_tutorias (id_fpxm, id_salon, id_usuario, id_estado_tutoria, cupos, tema, fecha, hora_inicial, hora_final)
                VALUES (%s,%s,%s,%s,%s,%s,%s, %s,%s)

                            


    """,(id_fpxm, horario.id_salon,id_usuario,6,horario.cupos,horario.tema,horario.fecha,horario.hora_inicial,horario.hora_final))
        bd.commit()
        cursor.close()
      
def getIdForData(salon:str):
    try:
        bd=get_db_connection()
        cursor=bd.cursor()
        sql="select s.id_salon from salones s where s.salon=%s "
        cursor.execute(sql,(salon,))
        id_salon=cursor.fetchone()[0]
        if(id_salon!=None):
            return {"success":id_salon}
        else:
            return {"error":"no se pudo encontrar el salon"}

    
    except Exception as e:
        return {"error":e}
    finally:
        cursor.close()
