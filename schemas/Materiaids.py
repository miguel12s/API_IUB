from pydantic import BaseModel

class MateriaIds(BaseModel):
    id_docente:int
    id_facultad:int
    id_programa:int