import os
from sqlalchemy import create_engine, MetaData, Table

# Configuración de la conexión a la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://conversiones_user:muses_c_us_27809@172.40.1.20:5432/prueba_api_conversiones")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)  # Cambiar a False en producción

# Metadata y tablas
metadata = MetaData()

ct = Table('conversion_temperatura', metadata, autoload_with=engine)