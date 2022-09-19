from flask import render_template
from app.controllers.helper import date_format
from app.controllers.queries.querys import comments

from app.blueprints.publication import blue_comments

import jwt
from jwt import exceptions
from functools import wraps
from flask import jsonify, request
#from flask_login import current_user
from flask import current_app
from app.controllers.queries.querys import get_public_id #,get_token 

#aun no se está en funcionamiento
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        
        try:
            # opción 1 usando cookie
            cookie = request.headers['Cookie']
            #print('--'*30)
            #print(cookie)
            cookie = cookie.split(sep=';')
            #print(cookie)
            token = [valor for valor in cookie if 'token' in valor and valor.startswith(' token')][0]
            #print(token)
            token = [tuple(token.strip().split(sep='='))]
            #print(token)
            token = dict(token)
            #print(token)
            #print('--'*30)
            # opción 2 usando session
            #from flask import session
            #token = session['token']
            
            token = token['token']
            
        except:
            token = None
            
        #token = get_token.get_token(username=username)
        #print(token, type(token))
        print(token)
        if not token:
            return jsonify({'message': 'No estás autorizado'})

        try:
            data = jwt.decode(token, key= current_app.config["SECRET_KEY"],
                       algorithms=["HS256"])
            usuario = get_public_id.get_public_id(data=data['tokens_jwt'])
            print(usuario)
        except exceptions.DecodeError as e:
            return jsonify({'message': f'el token es invalido {e}'})
        
        return f(usuario,*args, **kwargs)
        
    return decorator


@blue_comments.route('/Publicaciones',methods = ['GET'])
@token_required
def publication_noapi(usuario):
    return render_template('publication.html', comments = comments.get_comment(), date_format = date_format)




