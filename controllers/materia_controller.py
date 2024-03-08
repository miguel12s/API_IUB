import mysql.connector
from fastapi import HTTPException
from config.db_config import get_db_connection
from schemas.Materia import Materia
from fastapi.encoders import jsonable_encoder
from models.admin import ModelAdmin
from schemas.Materiaids import MateriaIds

class MateriaController:
    
    def getMaterias():
        try:
           rpta= ModelAdmin.getMaterias()
           return rpta       
        except Exception as e :
            print(e)

    def getMateria(id_materia: int):
        try:
           print('entrastes')
           rpta= ModelAdmin.getMateria(id_materia)
           print(rpta)
           return rpta       
        except Exception as e :
            print(e)
            

    def createMateria(materia: Materia):
        try:
           rpta= ModelAdmin.createMateria(materia)
           return rpta       
        except Exception as e :
            print(e)
    
    def updateMateria(materia:Materia,id:int):
        try:
           rpta= ModelAdmin.updateMateria(materia,id)
           return rpta       
        except Exception as e :
            print(e)
    def getMateriaForIds(materiaids:MateriaIds):
        try:
            rpta=ModelAdmin.getMateriaForIds(materiaids)
            return rpta
        except Exception as e:
            return HTTPException(status_code=500,detail=e)
    


