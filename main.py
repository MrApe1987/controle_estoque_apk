from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from random import random
import json
import os


class EstoqueScreen(Screen):
    pass


class HistoricoScreen(Screen):
    pass


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
        btn_menos.bind(on_release=self.diminuir)

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

    def diminuir(self, *args):
        if self.quantidade > 0:
            self.quantidade -= 1
            self.atualizar_texto()
            MDApp.get_running_app().salvar_produtos()

    def remover(self, *args):
        if self.parent:
            self.parent.remove_widget(self)
            MDApp.get_running_app().salvar_produtos()


class EstoqueApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("interfaces/main.kv")

    def on_start(self):
        Clock.schedule_once(self.carregar_produtos, 0.3)

    # --------------------------
    # ADICIONAR PRODUTO
    # --------------------------
    def adicionar_produto(self):
        tela = self.root.get_screen("estoque")

        nome = tela.ids.campo_nome.text.strip()
        quantidade = tela.ids.campo_quantidade.text.strip()
        local = tela.ids.campo_local.text.strip()

        if nome and quantidade.isdigit() and local:
            item = ProdutoItem(nome, int(quantidade), local)
            tela.ids.lista_produtos.add_widget(item)

            tela.ids.campo_nome.text = ""
            tela.ids.campo_quantidade.text = ""
            tela.ids.campo_local.text = ""

            self.salvar_produtos()

    # --------------------------
    # SALVAR JSON
    # --------------------------
    def salvar_produtos(self):
        tela = self.root.get_screen("estoque")
        produtos = []

        for item in tela.ids.lista_produtos.children:
            produtos.append({
                "nome": item.nome,
                "quantidade": item.quantidade,
                "local": item.local
            })

        with open("produtos.json", "w", encoding="utf-8") as f:
            json.dump(produtos, f, ensure_ascii=False, indent=2)

    # --------------------------
    # CARREGAR JSON
    # --------------------------
    def carregar_produtos(self, *args):
        tela = self.root.get_screen("estoque")

        if os.path.exists("produtos.json"):
            with open("produtos.json", "r", encoding="utf-8") as f:
                for dic in json.load(f):
                    tela.ids.lista_produtos.add_widget(
                        ProdutoItem(
                            dic["nome"],
                            dic["quantidade"],
                            dic["local"]
                        )
                    )

    # --------------------------
    # RELATÓRIO
    # --------------------------
    def gerar_relatorio(self):
        texto = "RELATÓRIO DE ESTOQUE\n\n"

        if os.path.exists("produtos.json"):
            with open("produtos.json", "r", encoding="utf-8") as f:
                for dic in json.load(f):
                    texto += f"{dic['nome']} - {dic['local']} - {dic['quantidade']}\n"

        tela = self.root.get_screen("historico")
        tela.ids.relatorio_container.clear_widgets()
        tela.ids.relatorio_container.add_widget(
            MDLabel(text=texto, adaptive_height=True)
        )

    # --------------------------
    # GRÁFICO DASHBOARD COMPLETO
    # --------------------------
    def gerar_grafico(self):

        tela = self.root.get_screen("historico")
        layout = tela.ids.relatorio_container
        layout.clear_widgets()

        dados = []

        if os.path.exists("produtos.json"):
            with open("produtos.json", "r", encoding="utf-8") as f:
                dados = json.load(f)

        if not dados:
            layout.add_widget(MDLabel(text="Nenhum produto cadastrado."))
            return

        scroll = ScrollView(
            do_scroll_x=True,
            do_scroll_y=False,
            size_hint=(1, None),
            height=dp(420)
        )

        grafico = Widget(size_hint=(None, None), height=dp(400))
        grafico.width = dp(len(dados) * 100)

        scroll.add_widget(grafico)
        layout.add_widget(scroll)

        max_qtd = max(p["quantidade"] for p in dados)

        largura_barra = dp(50)
        espacamento = dp(40)
        base_x = dp(60)
        base_y = dp(100)

        barras = []

        with grafico.canvas:

            # Linha base
            Color(0.7, 0.7, 0.7, 1)
            Rectangle(pos=(dp(30), base_y - dp(5)), size=(grafico.width, dp(2)))

            for i, produto in enumerate(dados):

                qtd = produto["quantidade"]
                altura_final = (qtd / max_qtd) * dp(220)

                x = base_x + i * (largura_barra + espacamento)
                y = base_y

                r = 0.3 + random() * 0.7
                g = 0.3 + random() * 0.7
                b = 0.3 + random() * 0.7

                Color(r, g, b, 1)
                barra = Rectangle(pos=(x, y), size=(largura_barra, 0))
                barras.append((barra, altura_final))

        # animação
        for barra, altura in barras:
            Animation(size=(barra.size[0], altura), duration=0.8).start(barra)

        # labels
        for i, produto in enumerate(dados):

            qtd = produto["quantidade"]
            altura = (qtd / max_qtd) * dp(220)

            x = base_x + i * (largura_barra + espacamento)

            valor_label = MDLabel(
                text=str(qtd),
                halign="center",
                size_hint=(None, None),
                size=(largura_barra, dp(30)),
                pos=(x, base_y + altura + dp(5)),
            )

            nome_label = MDLabel(
                text=produto["nome"],
                halign="center",
                size_hint=(None, None),
                size=(largura_barra + dp(20), dp(40)),
                pos=(x - dp(10), dp(30)),
                theme_text_color="Secondary"
            )

            grafico.add_widget(valor_label)
            grafico.add_widget(nome_label)

    # --------------------------
    # TROCAR TELAS
    # --------------------------
    def abrir_historico(self):
        self.root.current = "historico"

    def voltar_estoque(self):
        self.root.current = "estoque"


EstoqueApp().run()
