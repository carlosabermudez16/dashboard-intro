import os
from dotenv import load_dotenv



load_dotenv()



class Config(object):
    # creamos un identificaor para nuestro formulario
    # cuando se valide del request por parte del servidor hay que validar
    # que el id haga match con el que se envío en el request
    SECRET_KEY = os.getenv("SECRET_KEY") # debe ir en el archivo env
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    
    host = os.getenv("HOST")
    database = os.getenv("DATABASE") 
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    port = os.getenv("PORT")
    driver = os.getenv("DRIVER")
    
    mail_port = int(os.environ.get('MAIL_PORT'))
    MAIL_SERVER   = os.getenv('MAIL_SERVER')
    MAIL_PORT     = mail_port or 465
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS  = False
    MAIL_USE_SSL  = True
    
    DATABASE_CONNECT_OPTIONS = {}
    
    # Hilos de aplicación. Una suposición general común es usar 2 por cada 
    # núcleo de procesador disponible: para manejar las solicitudes entrantes 
    # usando uno y realizar operaciones en segundo plano usando el otro.
    THREADS_PER_PAGE = 2
    
    
    # Habilite la protección contra *Falsificación de solicitud entre sitios (CSRF)*
    CSRF_ENABLED     = True
    # Utilice una clave segura, única y absolutamente secreta para firmar los datos.
    CSRF_SESSION_KEY = "secret"


class DevelopmentConfig(Config):
    valor = 0
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:123456@localhost:5432/flask_CF'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    
class ProductionConfig(Config):
    valor = 1
    SQLALCHEMY_DATABASE_URI = f'{Config.driver}://{Config.user}:{Config.password}@{Config.host}/{Config.database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    DEBUG = False    

        
    
    
    
    
    
    
    
    
    