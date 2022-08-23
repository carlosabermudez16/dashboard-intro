from flask import flash, request, render_template
from app.views.forms import CommentForm
from app.controllers.queries.querys import comments
from app.controllers.helper import date_format
from flask_login import current_user, login_required

from app.blueprints.dashboard import blue_dashboard

@blue_dashboard.route('/dashboard', methods = ['GET','POST'])
@login_required
def dashboard():
    
    comment_form = CommentForm(request.form)
    
    try:
        if request.method == 'POST' and comment_form.validate():
            from app.controllers.queries.querys import save_comment
            
            user_id = current_user.id
            
            save_comment.post_comment(user_id=user_id,text=comment_form.comment.data)
            
            success_message = 'Nuevo comentario creado!'
            flash(success_message)
            
            
    except :
        flash('Hay un problema en la publicación del comentario!')    
    
    return render_template('dashboard.html', usuario = current_user.username, form = comment_form,comments = comments.get_comment(), date_format = date_format)

from flask import Response
import pandas as pd
@blue_dashboard.route('/descargar_reporte')
@login_required
def download():
    datos = comments.get_comment()
    lista = []
    for data in datos:
        dic = {}
        dic['id'] = data.id
        dic['date'] = data.created_date
        dic['name'] = data.username
        dic['text'] = data.text
        lista.append(dic)
    df = pd.DataFrame(lista)
    #df.set_index('id',inplace=True)
    
    return Response(df.to_csv(),mimetype="text/csv",headers={"Content-Disposition":"attachment; filename=reporte_personas.csv"})

from flask import current_app, redirect,url_for
from werkzeug.utils import secure_filename
import os
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

def allowed_file(file):
    file = file.split('.')
    if file[1] in ALLOWED_EXTENSIONS:
        return True
    return False

@blue_dashboard.route('/upload', methods=['POST'])
@login_required
def upload():
    current_app.config['UPLOAD_FOLDER'] = "\\app\\static\\blueprint_static\\dashboard_static\\static\\uploads"
    file = request.files["uploadFile"]
    filename = secure_filename(file.filename)
    ruta = os.getcwd()+current_app.config['UPLOAD_FOLDER']+f'\\{filename}'
    
    try:
        if file and allowed_file(filename):
            file.save(ruta)
            success_message = 'Archivo cargado exitosamente!'
    except:
        success_message = 'No se subío ningún archivo'
    
    flash(success_message)
    
    return redirect(url_for('blue_dashboard.dashboard'))
    