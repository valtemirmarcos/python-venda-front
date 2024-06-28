import os
import requests
from flask import session

class usuariosController:
    def logar(self, jsonEntrada):
        urlLogar = f"{os.getenv('URL_API')}/login"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(urlLogar, json=jsonEntrada, headers=headers)
        
        return response

    def exibirDadosUsuarioLogado(self):
        token = session['auth_token']
        urlLogado = f"{os.getenv('URL_API')}/usuarios/dadosCadastrados"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(urlLogado, headers=headers)
        return response
    
    def listarEnderecos(self):
        token = session['auth_token']
        urlEnderecos = f"{os.getenv('URL_API')}/usuarios/listarEnderecos"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(urlEnderecos, headers=headers)
        return response

    def addFavoritos(self, produto_id):
        token = session['auth_token']
        urlAddFavoritos = f"{os.getenv('URL_API')}/usuarios/favoritos/gravar"
        jsonProduto = {
            "produto_id":produto_id
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.post(urlAddFavoritos, json=jsonProduto, headers=headers)

        return response

    def removeFavoritos(self, produto_id):
        token = session['auth_token']
        urlRemoveFavoritos = f"{os.getenv('URL_API')}/usuarios/favoritos/remover"
        jsonProduto = {
            "produto_id":produto_id
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.post(urlRemoveFavoritos, json=jsonProduto, headers=headers)

        return response

    def listarFavoritos(self):
        token = session['auth_token']
        urlFavoritos = f"{os.getenv('URL_API')}/usuarios/favoritos"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(urlFavoritos, headers=headers)
        return response

    def listarPedidos(self):
        token = session['auth_token']
        urlPedidos = f"{os.getenv('URL_API')}/vendas/pedidos"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(urlPedidos, headers=headers)
        return response

    def alterarSenha(self, json):
        token = session['auth_token']
        urlSenha = f"{os.getenv('URL_API')}/login/alterarSenha"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.post(urlSenha, json=json, headers=headers)

        return response
        
    def enviarEmailContato(self, json):
        urlContato = f"{os.getenv('URL_API')}/enviarEmail"
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(urlContato, json=json, headers=headers)
        return response