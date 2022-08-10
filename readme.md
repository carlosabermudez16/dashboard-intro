
flask run --cert=adhoc --> para https

flask db init --> se ejecuta una única vez
flask db upgrade --> cada vez que hay un cambio en el modelo
flask db migrate --> realiza la modificación en la base de datos

set FLASK_APP = wsgi:app
flask run