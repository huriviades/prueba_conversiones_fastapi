from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.engine import Result
from database.database import engine, ct
from schemas.schemas import ConversionTemperaturaSchema
from typing import List

####################################### Router para diferentes temperaturas
temperatura_router = APIRouter()

@temperatura_router.get("/api/conversiones/temperatura", response_model=List[ConversionTemperaturaSchema])
def get_conversion_temperatura():
    try:
        with engine.connect() as connection:
            query = select(ct)
            result: Result = connection.execute(query)
            resultados = [ConversionTemperaturaSchema(**dict(zip(result.keys(), row))) for row in result]
            return resultados
    except Exception as e:
        print(f"Error inesperado: {e}")  # Imprimir el error en la consola
        raise HTTPException(status_code=500, detail="Error al consultar la base de datos.")
    
@temperatura_router.post("/api/conversiones/temperatura", response_model=ConversionTemperaturaSchema)
def create_conversion_temperatura(conversion: ConversionTemperaturaSchema):
    try:
        with engine.connect() as connection:
            # Crear la sentencia de inserción
            stmt = insert(ct).values(
                resultado=conversion.resultado,
                tipo=conversion.tipo,
            )
            result: Result = connection.execute(stmt)
            connection.commit()
            conversion.id = result.inserted_primary_key[0]  # Esto asume que el ID es autoincremental
            return conversion
    except Exception as e:
        print(f"Error inesperado: {e}")  # Imprimir el error en la consola
        raise HTTPException(status_code=500, detail="Error al insertar datos en la base de datos.")

@temperatura_router.put("/api/conversiones/temperatura/{id}", response_model=ConversionTemperaturaSchema)
def update_conversion_temperatura(id: int, conversion: ConversionTemperaturaSchema):
    try:
        with engine.connect() as connection:
            query = select(ct).where(ct.c.id == id)
            result: Result = connection.execute(query)
            existing = result.fetchone()

            if not existing:
                raise HTTPException(status_code=404, detail="Registro no encontrado.")
            
            stmt = update(ct).where(ct.c.id == id).values(
                resultado = conversion.resultado,
                tipo = conversion.tipo,
            )
            
            connection.execute(stmt)
            connection.commit()

            conversion.id = id
            return conversion
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error inesperado: {e}")  # Imprimir el error en la consola
        raise HTTPException(status_code=500, detail="Error al actualizar datos en la base de datos.")     

@temperatura_router.delete("/api/conversiones/temperatura/{id}")
def delete_conversion_temperatura(id: int):
    try:
        with engine.connect() as connection:
            query = select(ct).where(ct.c.id == id)
            result: Result = connection.execute(query)
            existing = result.fetchone()

            if not existing:
                raise HTTPException(status_code=404, detail="Registro no encontrado.")
            
            stmt = delete(ct).where(ct.c.id == id)
            connection.execute(stmt)
            connection.commit()

            return {"message": f"Registro con id {id} eliminado correctamente."}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar datos en la base de datos.")     

