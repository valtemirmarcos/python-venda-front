from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from controllers.produtosController import produtosController
from controllers.usuariosController import usuariosController
import requests
import os
from babel.numbers import format_currency
from functools import wraps
from rotas.auth import login_required

carrinho_bp = Blueprint('carrinho',__name__,template_folder='templates')

@carrinho_bp.route('/')
@login_required
def carrinho():
    return render_template('carrinho.html')

@carrinho_bp.route('/addCarrinho')
@login_required
def addCarrinho():
    idProd = request.args.get('idProd')
    produtos_ctl = produtosController()
    dados = produtos_ctl.produto(idProd).json()
    jsonProduto = {}
    if dados['status'] != 'success':
        return render_template('erro404.html')
    if 'dados_carrinho' not in session:
        session['dados_carrinho'] = {}

    session['dados_carrinho'][idProd] = dados['data']
    
    session.modified = True

    return redirect(url_for('carrinho.carrinho'))
    


@carrinho_bp.route('/excluirItem/<int:idProd>')
def carrinhoExcluirItem(idProd):
    nid = str(idProd)
    del session['dados_carrinho'][nid]
    session.modified = True
    return redirect(url_for('carrinho.carrinho'))

# @carrinho_bp.route('/carrinho/addQtde')
# def carrinhoAddQtde():
#     return "ok"
#     return redirect(url_for('carrinho.carrinho'))

@carrinho_bp.route('/enviarJson',methods=['POST'])
def carrinhoEnviarJson():
    data=[]
    if request.method == 'POST':
        data = request.get_json()
    session["compra"] = data
    session["dados_compra"] = {
        'compra':data,
        'itens':session['dados_carrinho']
    }
    return {"status":"success","dados_compra":session["dados_compra"]}



@carrinho_bp.route('/fechar-compra')
def fecharCompra():
    produtos_ctl = produtosController()
    dados = produtos_ctl.listarItensComprados(session["dados_compra"])
    session['itens_gerais'] = dados
    return render_template('fechar_compra.html', compras=dados)

@carrinho_bp.route('/fechar-compra/addFrete', methods=['POST'])
def fecharCompraAddFrete():
    frete = 11
    session["dados_compra"]["compra"]["frete"] = frete
    session.modified = True

    return redirect(url_for('carrinho.fecharEndereco', frete=frete))

@carrinho_bp.route('/fechar-endereco', methods=['GET','POST'])
def fecharEndereco():
    usuarios_ctl = usuariosController()
    dadosEnderecos = usuarios_ctl.listarEnderecos().json()
    if dadosEnderecos.get('status')!='success':
        return redirect(url_for('auth.login')) 
    enderecos = dadosEnderecos.get('data')
    frete = request.args.get('frete', '0.00')

    return render_template('fechar_endereco.html',enderecos=enderecos,frete=frete)

@carrinho_bp.route('/fechar-pagamento')
def fecharPagamento():
    return render_template('fechar_pagamento.html')

@carrinho_bp.route('/fechar-pedido')
def fecharPedido():
    jsonEntrada = {
        "endereco_id":session['dados_usuario']['id_endereco'],
        "pagamento_id":1,
        "valor_frete":float(session['dados_compra']['compra']['frete']),
    }
    jsonEntradaItens = []
    for item in session["dados_compra"]['compra']['itens']:
        jsonItens = {
           "produto_id":item["idProduto"],
           "tipo_pagamento":"Cartao",
           "quantidade":float(item["qtde"]),
           "valor_total":item["calculado"],
           "obs":item["produto"]
        }
        jsonEntradaItens.append(jsonItens)
    
    jsonEntrada['itens'] = jsonEntradaItens
    produtos_ctl = produtosController()
    gerarPedido = produtos_ctl.gerarPedido(jsonEntrada).json()
    if gerarPedido['status']!='success':
        erro="falhar ao concluir o pedido"
        return redirect(url_for('fecharPagamento', erro=erro))

    dados = gerarPedido['data']
    session.pop('dados_compra', None)
    session.pop('compra', None)
    session.pop('itens', None)
    session.pop('dados_carrinho', None)
    session.pop('itens_gerais', None)
    

    return render_template('fechar_pedido.html', dados=dados)    
