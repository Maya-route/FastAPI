from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
import psycopg2
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine (SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker (autoflush=False , autocommit = False , bind=engine)

Base = declarative_base()

def get_db ():
    
    db = SessionLocal() 
    try: 
        yield db
    finally: 
        db.close 
'''           
while True:
    try :
        conn = psycopg2.connect(host='localhost', database='FastAPI', 
        user='postgres', password = 'Medanfikre1', cursor_factory=RealDictCursor)
        cursor = conn.cursor() # this is used for executing  the SQL statements , queries 
        print("Connection Successful")
        break
    except Exception as error:
        print('Database connection Failed ')
        print(f'Error {error}')
        time.sleep(3)
        
this part is commented out as we are ot using it anymore we are actually using sqlalchamy our choice of ORM for DB connectivity
'''