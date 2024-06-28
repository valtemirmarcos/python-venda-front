from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from controllers.produtosController import produtosController
from controllers.usuariosController import usuariosController
import requests
import os
from babel.numbers import format_currency
from functools import wraps

contatos_bp = Blueprint('contato',__name__,template_folder="templates")

usuarios_ctl = usuariosController()

@contatos_bp.route('/')
def contato():
    return render_template('contato.html')

@contatos_bp.route('/confirmacao', methods=['GET','POST'])
def confirmContato():
    mensagensErros=""
    erros = []
    if 'txtNomeCompleto' not in request.form or not request.form['txtNomeCompleto'].strip():
        erros.append("Peencha seu nome")
    
    if 'txtEmail' not in request.form or not request.form['txtEmail'].strip():
        erros.append("Preencha um e-mail valido")

    if 'txtMensagem' not in request.form or not request.form['txtMensagem'].strip():
        erros.append("preencha o assunto")

    mensagensErros = ' ,'.join(erros)
    
    if erros:
        return render_template('contato.html', erros=mensagensErros)

    jsonMensagem = {
        "nome":request.form['txtNomeCompleto'],
        "email":"valtemir.pereira@d2p.com.br",
        "assunto":"Contato - Cliente",
        "conteudo":(
            f"Recebemos a duvida de {request.form['txtNomeCompleto']} \n"
            f"Responder para o email:{request.form['txtEmail']} \n"
            f"Duvida: \n {request.form['txtMensagem']}"
        )  ,
        "emailResp":request.form['txtEmail']
    }
    enviarEmailContato = usuarios_ctl.enviarEmailContato(jsonMensagem).json()

    return render_template('confirmcontato.html',json=jsonMensagem)