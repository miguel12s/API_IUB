from pydantic import BaseModel


class Solicitud(BaseModel):
    id_peti_hora:int=None
    id_docente:int
    id_salon:int
    fecha:str
    hora_inicial:str
    hora_final:str
    id_facultad:int
    id_programa:int
    id_materia:int
    id_capacidad:int
    tema:str
    