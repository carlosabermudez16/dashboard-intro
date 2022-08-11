from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail

from config.config import DevelopmentConfig, ProductionConfig, CloudDev

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
mail = Mail()

def create_app(config_class):
    app = Flask(__name__, template_folder='templates')
    
    
    try:
        if config_class == 'prod':
            configuration = ProductionConfig
            
        elif  config_class == 'dev':
            configuration = DevelopmentConfig
        elif config_class == 'cloud':
            configuration = CloudDev
    except:
        print('hubo un error en la configuración')

    app.config.from_object(configuration)

    login_manager.session_protection = "strong"
    login_manager.login_view = 'rg.loggin'
    login_manager.init_app(app)
    csrf.init_app(app=app)
    db.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)
    #CORS(app, support_credentials=True)
    
    # configuración base de datos
    from app.database.setup import create_tables
    create_tables(app=app, db=db, config_class=config_class)
    
    from app.models.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    
    from app.blueprints.home import blue_home
    from app.controllers.api.apis import blue_api
    from app.blueprints.auth import blue_rg
    from app.blueprints.publication import blue_comments
    from app.blueprints.dashboard import blue_dashboard
    app.register_blueprint(blue_home)
    app.register_blueprint(blue_rg)
    app.register_blueprint(blue_dashboard)
    app.register_blueprint(blue_comments)
    app.register_blueprint(blue_api)
    
    
    
    
    
    # plantilla de error para las ruta que no existen
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    return app




