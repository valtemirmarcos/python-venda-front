from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from controllers.produtosController import produtosController
from controllers.usuariosController import usuariosController
import requests
import os
from babel.numbers import format_currency
from functools import wraps

auth_bp = Blueprint('auth',__name__,template_folder='templates')

@auth_bp.route('/login')
def login():
    return render_template('login.html')
   
@auth_bp.route('/logar', methods=['GET', 'POST'])
def logar():
    if request.method == 'POST':
        jsonEntrada = {
            'email': request.form.get('txtEmail'),
            'password': request.form.get('txtSenha')
        }
        usuarios_ctl = usuariosController()
        response = usuarios_ctl.logar(jsonEntrada)
        try:
            logar = response.json()
            if logar['status'] != 'success':
                ardados = logar['data'].split(":")
                return render_template('login.html', erro=logar, dados=ardados[1])
            session['auth_token'] = logar['data']  
            session['logado'] = True
            session.modified = True
            return redirect(url_for('produtos.index'))
        except requests.exceptions.JSONDecodeError:
            return jsonify({'error': 'Erro ao decodificar a resposta JSON'}), 500
    else:
        return render_template('login.html')


# Decorador de verificação de login
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logado' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrap

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('auth_token', None)
    session.pop('dados_usuario', None)
    session.pop('logado', None)
    # session.pop('urlApi', None)
    return redirect(url_for('auth.login'))



@auth_bp.route('/recuperarsenha')
def recuperarSenha():
    return render_template('recuperar_senha.html')    

@auth_bp.route('/confirmrecupsenha')
def confirmRecupSenha():
    return render_template('confirmrecupsenha.html')  