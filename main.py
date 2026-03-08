from kivy.config import Config

Config.set('input', 'mouse', 'mouse')
Config.set('input', 'mtdev', '')
Config.set('kivy', 'log_level', 'warning')

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock

import json
import os


# TELAS
class LoginScreen(Screen):
    pass


class RegisterScreen(Screen):
    pass


class EstoqueScreen(Screen):
    pass


class HistoricoScreen(Screen):
    pass


# ITEM PRODUTO
class ProdutoItem(MDCard):

    def __init__(self, nome="", quantidade=0, local="", **kwargs):
        super().__init__(**kwargs)

        self.nome = nome
        self.quantidade = quantidade
        self.local = local

        self.size_hint_y = None
        self.height = "100dp"
        self.padding = 10
        self.radius = [15]
        self.elevation = 3

        layout = MDBoxLayout(orientation="horizontal", spacing=10)

        self.label = MDLabel()

        btn_menos = MDIconButton(icon="minus")
        btn_menos.bind(on_release=self.retirar)

        btn_mais = MDIconButton(icon="plus")
        btn_mais.bind(on_release=self.aumentar)

        btn_delete = MDIconButton(icon="delete")
        btn_delete.bind(on_release=self.remover)

        layout.add_widget(self.label)
        layout.add_widget(btn_menos)
        layout.add_widget(btn_mais)
        layout.add_widget(btn_delete)

        self.add_widget(layout)

        self.atualizar_texto()

    def atualizar_texto(self):

        self.label.text = f"{self.nome}\nLocal: {self.local} | Estoque: {self.quantidade}"

        if self.quantidade <= 2:
            self.label.theme_text_color = "Custom"
            self.label.text_color = (1, 0, 0, 1)
        else:
            self.label.theme_text_color = "Primary"

    def aumentar(self, *args):

        self.quantidade += 1
        self.atualizar_texto()

        MDApp.get_running_app().salvar_produtos()

    # POPUP PARA RETIRADA
    def retirar(self, *args):

        app = MDApp.get_running_app()

        campo = MDTextField(
            hint_text="Quantidade a retirar",
            input_filter="int"
        )

        def confirmar(*args):

            if campo.text.isdigit():

                qtd = int(campo.text)

                if qtd <= self.quantidade:

                    self.quantidade -= qtd
                    self.atualizar_texto()

                    app.registrar_retirada(self.nome, qtd)

                    app.salvar_produtos()

            dialog.dismiss()

        dialog = MDDialog(
            title="Retirar produto",
            type="custom",
            content_cls=campo,
            buttons=[
                MDFlatButton(
                    text="Cancelar",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDFlatButton(
                    text="Confirmar",
                    on_release=confirmar
                ),
            ],
        )

        dialog.open()

    def remover(self, *args):

        if self.parent:
            self.parent.remove_widget(self)

        MDApp.get_running_app().salvar_produtos()


# APP
class EstoqueApp(MDApp):

    usuario_logado = ""

    def build(self):

        self.theme_cls.primary_palette = "Blue"

        return Builder.load_file("interfaces/main.kv")

    def on_start(self):

        Clock.schedule_once(self.carregar_produtos, 0.2)

    # LOGIN
    def login(self):

        tela = self.root.get_screen("login")

        usuario = tela.ids.usuario.text
        senha = tela.ids.senha.text

        if os.path.exists("usuarios.json"):

            with open("usuarios.json", "r") as f:
                usuarios = json.load(f)

                if usuario in usuarios and usuarios[usuario] == senha:

                    self.usuario_logado = usuario
                    self.root.current = "estoque"

    # REGISTRO
    def registrar_usuario(self):

        tela = self.root.get_screen("register")

        usuario = tela.ids.usuario.text
        senha = tela.ids.senha.text

        usuarios = {}

        if os.path.exists("usuarios.json"):

            with open("usuarios.json", "r") as f:
                usuarios = json.load(f)

        usuarios[usuario] = senha

        with open("usuarios.json", "w") as f:
            json.dump(usuarios, f)

        self.root.current = "login"

    # LOGOUT
    def logout(self):

        self.usuario_logado = ""
        self.root.current = "login"

    # ADICIONAR PRODUTO
    def adicionar_produto(self):

        tela = self.root.get_screen("estoque")

        nome = tela.ids.campo_nome.text
        quantidade = tela.ids.campo_quantidade.text
        local = tela.ids.campo_local.text

        if nome and quantidade.isdigit():

            item = ProdutoItem(nome, int(quantidade), local)

            tela.ids.lista_produtos.add_widget(item)

            tela.ids.campo_nome.text = ""
            tela.ids.campo_quantidade.text = ""
            tela.ids.campo_local.text = ""

            self.salvar_produtos()

    # SALVAR PRODUTOS
    def salvar_produtos(self):

        tela = self.root.get_screen("estoque")

        produtos = []

        for item in tela.ids.lista_produtos.children:

            produtos.append({
                "nome": item.nome,
                "quantidade": item.quantidade,
                "local": item.local
            })

        with open("produtos.json", "w") as f:
            json.dump(produtos, f)

    # CARREGAR PRODUTOS
    def carregar_produtos(self, *args):

        tela = self.root.get_screen("estoque")

        if os.path.exists("produtos.json"):

            with open("produtos.json", "r") as f:

                for dic in json.load(f):

                    tela.ids.lista_produtos.add_widget(
                        ProdutoItem(
                            dic["nome"],
                            dic["quantidade"],
                            dic["local"]
                        )
                    )

    # HISTÓRICO
    def registrar_retirada(self, produto, qtd):

        historico = []

        if os.path.exists("historico.json"):

            with open("historico.json", "r") as f:
                historico = json.load(f)

        historico.append({
            "usuario": self.usuario_logado,
            "produto": produto,
            "quantidade": qtd
        })

        with open("historico.json", "w") as f:
            json.dump(historico, f)

    # ABRIR HISTÓRICO
    def abrir_historico(self):

        tela = self.root.get_screen("historico")

        tela.ids.relatorio_container.clear_widgets()

        if os.path.exists("historico.json"):

            with open("historico.json", "r") as f:

                historico = json.load(f)

                for h in historico:

                    texto = f"{h['usuario']} retirou {h['quantidade']} {h['produto']}"

                    tela.ids.relatorio_container.add_widget(
                        MDLabel(
                            text=texto,
                            adaptive_height=True
                        )
                    )

        self.root.current = "historico"

    def voltar_estoque(self):

        self.root.current = "estoque"


EstoqueApp().run()
