from sqlalchemy import create_engine


def ruta_databse(entrypoint):
    driver = entrypoint.driver
    host= entrypoint.host
    user= entrypoint.user
    password= entrypoint.password
    database= entrypoint.database
    puerto = entrypoint.port
    
    ruta = f'{driver}://{user}:{password}@{host}:{puerto}/{database}'
    return ruta

def create_tables(app,db):
    
    valor = app.config['SQLALCHEMY_DATABASE_URI']
    
    try:
        with app.app_context():  # me permite sicronizar la base de datos con la aplicación
            if 'mysql' in valor:
                from config.config import ProductionConfig
                ruta = ruta_databse(entrypoint=ProductionConfig)
                print(ruta)
                engine = create_engine(ruta)
                
                name = 'Mysql'
                print(name)
            else:
                from config.config import DevelopmentConfig
                ruta = ruta_databse(entrypoint=DevelopmentConfig)
                print(ruta)
                engine = create_engine(ruta)
                
                name = 'Postgresql'
                print(name)
                
            print(f"\nConexión a base de datos {name} exitosa!")
            db.metadata.create_all(engine)    # crea la tabla en la base de datos que se encuentra en la cadena de conexion(url)                
            print("Tabla creada exitosamente!\n")
        return True
    except:
        print(f"Error at create_tables()" )
    