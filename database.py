import pymssql
from sqlalchemy import create_engine
import pandas as pd

def db_data(query, DATABASE_CON):

    connection_data = DATABASE_CON
    connection = pymssql.connect(**connection_data)
    db_engine = create_engine(f'mssql+pymssql://{connection_data["user"]}:{connection_data["password"]}@{connection_data["server"]}/{connection_data["database"]}')
    df = pd.read_sql(query, db_engine)
    connection.close

    return df