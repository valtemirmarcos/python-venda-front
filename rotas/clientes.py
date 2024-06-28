from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from controllers.usuariosController import usuariosController

cliente_bp = Blueprint('cliente',__name__,template_folder='templates')

usuarios_ctl = usuariosController()

@cliente_bp.route('/pedidos')
def clientePedidos():
    listarPedidos = usuarios_ctl.listarPedidos().json()
    if 'status' not in listarPedidos or listarPedidos['status'] != 'success':
        return render_template('erro404.html')

    return render_template('cliente_pedidos.html', dados=listarPedidos['data'])

@cliente_bp.route('/dados')
def clienteDados():
    dados = usuarios_ctl.exibirDadosUsuarioLogado().json()
    if 'status' not in dados or dados['status'] != 'success':
        return render_template('erro404.html')
    
    return render_template('cliente_dados.html',dados=dados['data'])

@cliente_bp.route('/contatos')
def clienteContatos():
    dados = usuarios_ctl.exibirDadosUsuarioLogado().json()
    if 'status' not in dados or dados['status'] != 'success':
        return render_template('erro404.html')

    return render_template('cliente_contatos.html',dados=dados['data'])

@cliente_bp.route('/endereco')
def clienteEndereco():
    dados = usuarios_ctl.exibirDadosUsuarioLogado().json()
    if 'status' not in dados or dados['status'] != 'success':
        return render_template('erro404.html')

    return render_template('cliente_endereco.html',dados=dados['data'])

@cliente_bp.route('/favoritos')
def clienteFavoritos():
    listarFavoritos = usuarios_ctl.listarFavoritos().json()
    erro=None
    if 'status' not in listarFavoritos or  listarFavoritos['status'] != "success":
        erro = 1 
    return render_template('cliente_favoritos.html', dados=listarFavoritos['data'], erro=erro)

@cliente_bp.route('/senha')
def clienteSenha():
    return render_template('cliente_senha.html')

@cliente_bp.route('/confirmcadastrosenha', methods=['GET','POST'])
def clienteConfirmCadastroSenha():
    if request.method == 'POST':
        erros = []
        if 'txtSenhaAtual' not in request.form or not request.form['txtSenhaAtual'].strip():
            erros.append("faltou senha atual")

        if 'txtSenha' not in request.form or not request.form['txtSenha'].strip():
            erros.append("faltou a nova senha")

        if 'txtConfSenha' not in request.form or not request.form['txtConfSenha'].strip():
            erros.append("faltou repetir a nova senha")

        mensagens = ', '.join(erros)

        if erros:
            return render_template('cliente_senha.html', erro=mensagens)

        jsonSenha = {
            "senhaAtual":request.form.get('txtSenhaAtual'),
            "novaSenha":request.form.get('txtSenha'),
            "confSenha":request.form.get('txtConfSenha')
        }

        alterarSenha = usuarios_ctl.alterarSenha(jsonSenha).json()
        if alterarSenha['status']!='success':
            return render_template('cliente_senha.html', erro=alterarSenha['data'])

        session.pop('auth_token', None)
        session.pop('dados_usuario', None)
        session.pop('logado', None)

        return render_template('confirmcadastrosenha.html')

@cliente_bp.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@cliente_bp.route('/cadastro/confirmacao')
def confirmCadastro():
    return render_template('confirmarcadastro.html')


@cliente_bp.route('/addFavoritos/<int:produto_id>', methods=['GET','POST'])
def addFavoritos(produto_id):
    
    resposta = usuarios_ctl.addFavoritos(produto_id).json()

    return redirect(url_for('produtos.index'))

@cliente_bp.route('/removeFavoritos/<int:produto_id>', methods=['GET','POST'])
def removeFavoritos(produto_id):
    resposta = usuarios_ctl.removeFavoritos(produto_id).json()
    redirecionamento = request.args.get('favoritos')
    if 'favoritos' in request.args and redirecionamento=='1':
        return redirect(url_for('cliente.clienteFavoritos'))

    return redirect(url_for('produtos.index'))