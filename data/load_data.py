
from sqlalchemy import create_engine, text
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import pandas as pd
import json
from pandas import DataFrame
import geopandas  as gpd

def connect_baby():
    #logging.info(f'Datos cargados desde base relacional')
    print(f'Datos cargados desde base relacional')

    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    ENDPOINT = 'localhost'  # dirección del host
    USER = 'postgres'       # usuario de la base de datos
    PASSWORD = 'xd'         # contraseña del usuario
    PORT = 5434             # puerto mapeado de PostgreSQL en Docker
    DATABASE = 'classicmodels'   # nombre de la base de datos

    # Crear la URL de conexión
    DATABASE_URL = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"
    # Crear la conexión
    engine = create_engine(DATABASE_URL)
    return DATABASE_URL, engine

def get_df(tabla):
    engine=connect_baby()
    # Cargar datos en un DataFrame
    query = f"SELECT * FROM {tabla}"
    try:
        df = pd.read_sql_query(query, engine)
        #logging.info(f'Datos cargados desde PostgreSQL: {df.head()}')
        print(f'Datos cargados desde PostgreSQL: {df.head()}')

    except Exception as e:
        #logging.error(f"Error al cargar datos desde PostgreSQL: {e}")
        print(f"Error al cargar datos desde PostgreSQL: {e}")
    return df

def get_schemaa(db):
    context = db.get_context()
    return context

def get_db():
    db_uri, connection=connect_baby()
    db=SQLDatabase.from_uri(db_uri)
    return db