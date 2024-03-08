from pydantic import BaseModel

class PeticionAceptada(BaseModel):
    estado: str
    fecha: str
    hora_final: str
    hora_inicial: str
    id_estado: int
    id_peti_hora: int
    nombre_estudiante: str
    salon: str
    tema: str
    id_fpxm:int
    id_capacidad:int