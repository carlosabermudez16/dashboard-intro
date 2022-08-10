from sqlite3 import Error
from config.config import Config
from sqlalchemy import create_engine



def create_tables(app,db):
    driver = Config.driver
    host= Config.host
    user= Config.user
    password= Config.password
    database= Config.database
    puerto = Config.port
    
    valor = app.config['SQLALCHEMY_DATABASE_URI']
    
    try:
        with app.app_context():  # me permite sicronizar la base de datos con la aplicación
            if 'mysql' in valor:
                engine = create_engine(f'{driver}://{user}:{password}@{host}/{database}')
                
                name = 'Mysql'
            else:
                engine = create_engine(f'postgresql://postgres:123456@localhost:5432/flask_CF')
                name = 'Postgresql'
                
            print(f"\nConexión a base de datos {name} exitosa!")
            db.metadata.create_all(engine)    # crea la tabla en la base de datos que se encuentra en la cadena de conexion(url)                
            print("Tabla creada exitosamente!\n")
        return True
    except Error as e:
        print(f"Error at create_tables(): {str(e)}" )
    