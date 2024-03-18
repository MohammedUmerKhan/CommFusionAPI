from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Database:
    Base = declarative_base()

    def __init__(self, server, database, trusted_connection=False, username=None, password=None, default_realm=None):
        if trusted_connection:
            connection_string = f'mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&Integrated+Security=True'
        else:
            connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'

        if default_realm:
            connection_string += f'&SSPIProvider={default_realm}'

        print("Connecting to the database...")
        try:
            self.engine = create_engine(connection_string, echo=True)
            self.Session = sessionmaker(bind=self.engine)
            print("Database connection successful.")
        except Exception as e:
            print(f"Error connecting to the database: {str(e)}")
            raise

    def get_db(self):
        db = self.Session()
        try:
            yield db
        finally:
            db.close()

# Initialize the database object here
database = Database(server='UMERFAROOQ5522', database='CommFusionDB', trusted_connection=False,
                    username='sa', password='123', default_realm='1433')
