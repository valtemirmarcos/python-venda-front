import os
import requests
from flask import session


class produtosController:

    def __init__(self):
        self.filtroUsuario = ""
        if 'dados_usuario' in session and 'id_cliente' in session["dados_usuario"]:
            self.filtroUsuario = f"userId={session['dados_usuario']['id_cliente']}"
        
    def inicio(self):
        
        urlInicio = f"{os.getenv('URL_API')}/produtos?{self.filtroUsuario}"
        response = requests.get(urlInicio)

        return response

    def buscar(self, busca):
        urlBuscar = f"{os.getenv('URL_API')}/produtos?filtro={busca}&{self.filtroUsuario}"
        response = requests.get(urlBuscar)

        return response

    def ordenar(self, valor):
        filtro = "?ordenadesc=updated_at"
        if 'A' in valor:
            filtro = "?ordena=produto"

        if 'B' in valor:
            filtro = "?ordena=vlvenda"

        if 'C' in valor:
            filtro = "?ordenadesc=vlvenda"

        urlOrdenar = f"{os.getenv('URL_API')}/produtos{filtro}&{self.filtroUsuario}"
        
        response = requests.get(urlOrdenar)
        return response

    def paginar(self, pagina):
        urlPaginar = f"{os.getenv('URL_API')}/produtos?page={pagina}"
        response = requests.get(urlPaginar)
        return response

    def produto(self, id):
        urlProduto = f"{os.getenv('URL_API')}/produtos/{id}"
        response = requests.get(urlProduto)
        return response

    def listarItensComprados(self, jsonItens):
        compra = jsonItens['compra']
        itens = jsonItens['itens']
        for item in compra['itens']:
            idProduto = item['idProduto']
            if idProduto in itens:
                item_detalhes = itens[idProduto]
                item.update(item_detalhes)
        # le a parte do json de compra, pega o itens e separa pelo idproduto  e pega tudo que esta em itens e joga para compra

        return compra

    def gerarPedido(self, json):
        token = session['auth_token']
        urlVendas = f"{os.getenv('URL_API')}/vendas/gerar"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.post(urlVendas, json=json,headers=headers)
        return response