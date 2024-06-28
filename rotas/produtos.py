from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from controllers.produtosController import produtosController
from controllers.usuariosController import usuariosController
import requests
import os
from babel.numbers import format_currency
from functools import wraps

produtos_bp = Blueprint('produtos',__name__,template_folder='templates')

@produtos_bp.route('/')
def index():
    jsonUsuario = {}
    if 'auth_token' in session and session['auth_token']:
        usuarios_ctl = usuariosController()
        dados_usuario = usuarios_ctl.exibirDadosUsuarioLogado().json()
        session['dados_usuario'] = dados_usuario['data']
        session['contadorItens']=0
        if session.get('dados_carrinho'):
            session['contadorItens'] = len(session['dados_carrinho'])
        
    produtos_ctl = produtosController()
    dados = produtos_ctl.inicio().json()

    if dados['status'] != 'success':
        return render_template('erro404.html')
    session.modified = True
  
    return render_template('index.html',dados=dados['data'])

@produtos_bp.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        search_term = request.form.get('txtBuscar') # Access form data from 'busca' input field
        try:
            produtos_ctl = produtosController()
            dados = produtos_ctl.buscar(search_term).json()
            if dados['status'] != 'success':
                return render_template('erro404.html')

            return render_template('index.html',dados=dados['data'])

        except requests.exceptions.RequestException as e:
            # Handle API request errors
            error_message = f"Erro ao buscar produtos: {str(e)}"
            return render_template('erro404.html')

@produtos_bp.route('/ordenar', methods=['GET', 'POST'])
def ordenar():
    if request.method == 'POST':
        filtroOrdena = request.form.get('txOrdenar') 
        
        try:
            produtos_ctl = produtosController()
            dados = produtos_ctl.ordenar(filtroOrdena).json()
            if dados['status'] != 'success':
                return render_template('erro404.html')
            
            return render_template('index.html',dados=dados['data'])

        except requests.exceptions.RequestException as e:
            # Handle API request errors
            error_message = f"Erro ao buscar produtos: {str(e)}"
            return render_template('erro404.html')

@produtos_bp.route('/paginar', methods=['GET', 'POST'])
def paginar():
    filtroPagina = request.args.get('page')
    try:
        produtos_ctl = produtosController()
        dados = produtos_ctl.paginar(filtroPagina).json()
        if dados['status'] != 'success':
            return render_template('erro404.html')
        
        return render_template('index.html',dados=dados['data'])

    except requests.exceptions.RequestException as e:
            # Handle API request errors
            error_message = f"Erro ao buscar produtos: {str(e)}"
            return render_template('erro404.html')

    return filtroPagina

@produtos_bp.route('/produto/<int:id>')
def produto(id):
    try:
        produtos_ctl = produtosController()
        dados = produtos_ctl.produto(id).json()
        if dados['status'] != 'success':
            return render_template('erro404.html')
        
        return render_template('produto.html',dados=dados['data'])

    except requests.exceptions.RequestException as e:
            # Handle API request errors
            error_message = f"Erro ao buscar produtos: {str(e)}"
            return render_template('erro404.html')
