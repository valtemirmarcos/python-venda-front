from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from controllers.produtosController import produtosController
from controllers.usuariosController import usuariosController
import requests
import os
from babel.numbers import format_currency, format_decimal
from functools import wraps
from rotas.clientes import cliente_bp
from rotas.auth import auth_bp, login_required
from rotas.carrinho import carrinho_bp
from rotas.produtos import produtos_bp
from rotas.contatos import contatos_bp

from datetime import datetime


# Cria uma instância do aplicativo Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# filtros para adicionar no front
# aplicar formato em reais
@app.template_filter('currency')
def currency_format(value):
    return format_currency(value, 'BRL', locale='pt_BR')

@app.template_filter('numerico')
def numerico(value):
    return format_decimal(value, locale='pt_BR')

@app.template_filter('multiplicar')
def multiplicar_filter(value, multiplier):
    try:
        return float(value) * float(multiplier)
    except (ValueError, TypeError):
        return None

@app.template_filter('formatar_cep')
def formatar_cep(cep):
    # Remove caracteres não numéricos do CEP
    cep = ''.join(filter(str.isdigit, cep))

    # Insere o hífen no CEP formatado
    cep_formatado = f"{cep[:5]}-{cep[5:]}"

    return cep_formatado

@app.template_filter('zeroEsquerda')
def zeroEsquerda(numero):
    return str(numero).zfill(5)

@app.template_filter('dataFomatada')
def dataFomatada(dt):
    dt_obj = datetime.strptime(dt, '%a, %d %b %Y %H:%M:%S GMT')
    data_formatada = dt_obj.strftime('%d/%m/%Y')
    return data_formatada

@app.template_filter('dataGravacao')
def dataGravacao(dt):
    dt_obj = datetime.strptime(dt, '%a, %d %b %Y %H:%M:%S GMT')
    data_formatada = dt_obj.strftime('%Y-%m-%d')
    return data_formatada

# filtro de session para nao zerar a quantidade em carrinho
@app.template_filter('get_compra')
def get_compra(idProduto):
    if 'compra' in session and 'itens' in session["compra"]:
        for item in session.get('compra', {}).get('itens', []):
            if item['idProduto'] == idProduto:
                json = {
                    'calculado':item['calculado'],
                    'idProduto':idProduto,
                    'qtde':item['qtde'],
                    'valor_total':item['valor_total']
                }
                return json

    return None  # Default value if not found

# registrar o filtro
app.jinja_env.filters['get_compra'] = get_compra


# fim de filtros para o front

# Define uma rota para o caminho raiz ('/')

app.register_blueprint(produtos_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(cliente_bp, url_prefix='/cliente')
app.register_blueprint(carrinho_bp, url_prefix='/carrinho')
app.register_blueprint(contatos_bp, url_prefix='/contato')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)