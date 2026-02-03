import os
import sys  # <-- Necesario para la ruta del exe
import json
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup

Window.size = (800, 600)

# ============================
# CARGAR JSON CORRECTAMENTE
# ============================
# Esto reemplaza tu "with open('menu.json', ...)" original
if getattr(sys, 'frozen', False):
    # Si está en un exe
    base_path = sys._MEIPASS
else:
    # Si está ejecutándose como script normal
    base_path = os.path.dirname(__file__)

ruta_json = os.path.join(base_path, 'menu.json')

with open(ruta_json, 'r', encoding='utf-8') as f:
    datos = json.load(f)

productos = datos['productos']
# ============================

# ============================
# CLASES DE PANTALLA
# ============================

class PantallaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        titulo = Label(
            text='🍕 RESTAURANTE GOURMET 🍕',
            font_size='48sp',
            bold=True,
            size_hint_y=0.4
        )
        layout.add_widget(titulo)
        
        subtitulo = Label(
            text='Bienvenido a nuestro menú digital',
            font_size='24sp',
            size_hint_y=0.2
        )
        layout.add_widget(subtitulo)
        
        btn_menu = Button(
            text='VER MENÚ',
            font_size='24sp',
            size_hint_y=0.3,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_menu.bind(on_press=self.ir_a_categorias)
        layout.add_widget(btn_menu)
        
        self.add_widget(layout)
    
    def ir_a_categorias(self, instance):
        self.manager.current = 'categorias'


class PantallaCategorias(Screen):
    def __init__(self, productos, **kwargs):
        super().__init__(**kwargs)
        self.productos = productos
        self.categorias = list(set([p['categoria'] for p in productos]))
        self.categorias.sort()
    
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        titulo = Label(
            text='CATEGORÍAS',
            font_size='32sp',
            bold=True,
            size_hint_y=0.1
        )
        layout.add_widget(titulo)
        
        grid = GridLayout(
            cols=2,
            spacing=10,
            padding=10,
            size_hint_y=0.8
        )
        
        for categoria in self.categorias:
            btn = Button(
                text=categoria,
                font_size='20sp',
                background_color=(0.1, 0.5, 0.9, 1)
            )
            btn.bind(on_press=lambda x, cat=categoria: self.ver_productos(cat))
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        
        btn_volver = Button(
            text='← VOLVER',
            size_hint_y=0.1,
            background_color=(0.7, 0.2, 0.2, 1)
        )
        btn_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'inicio'))
        layout.add_widget(btn_volver)
        
        self.add_widget(layout)
    
    def ver_productos(self, categoria):
        self.manager.get_screen('productos').categoria_actual = categoria
        self.manager.current = 'productos'


class PantallaProductos(Screen):
    def __init__(self, productos, **kwargs):
        super().__init__(**kwargs)
        self.productos = productos
        self.categoria_actual = None
    
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        titulo = Label(
            text=f'CATEGORÍA: {self.categoria_actual}',
            font_size='28sp',
            bold=True,
            size_hint_y=0.1
        )
        layout.add_widget(titulo)
        
        scroll = ScrollView(size_hint_y=0.8)
        grid_productos = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        grid_productos.bind(minimum_height=grid_productos.setter('height'))
        
        productos_categoria = [p for p in self.productos if p['categoria'] == self.categoria_actual]
        
        for producto in productos_categoria:
            btn = Button(
                text=f"{producto['nombre']}\n${producto['precio']:.2f}",
                font_size='18sp',
                size_hint_y=None,
                height=80,
                background_color=(0.2, 0.7, 0.3, 1)
            )
            grid_productos.add_widget(btn)
        
        scroll.add_widget(grid_productos)
        layout.add_widget(scroll)
        
        btn_volver = Button(
            text='← VOLVER A CATEGORÍAS',
            size_hint_y=0.1,
            background_color=(0.7, 0.2, 0.2, 1)
        )
        btn_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'categorias'))
        layout.add_widget(btn_volver)
        
        self.add_widget(layout)


class RestauranteApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PantallaInicial(name='inicio'))
        sm.add_widget(PantallaCategorias(productos, name='categorias'))
        sm.add_widget(PantallaProductos(productos, name='productos'))
        return sm


if __name__ == '__main__':
    app = RestauranteApp()
    app.run()
