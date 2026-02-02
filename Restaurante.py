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
        
        # Botón para ver menú
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
    """Pantalla con las categorías de productos"""
    def __init__(self, productos, **kwargs):
        super().__init__(**kwargs)
        self.productos = productos
        self.categorias = list(set([p['categoria'] for p in productos]))
        self.categorias.sort()
    
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        titulo = Label(
            text='CATEGORÍAS',
            font_size='32sp',
            bold=True,
            size_hint_y=0.1
        )
        layout.add_widget(titulo)
        
        # Grid de categorías
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
        
        # Botón volver
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
    """Pantalla con productos de una categoría"""
    def __init__(self, productos, **kwargs):
        super().__init__(**kwargs)
        self.productos = productos
        self.categoria_actual = None
    
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título con categoría
        titulo = Label(
            text=f'CATEGORÍA: {self.categoria_actual}',
            font_size='28sp',
            bold=True,
            size_hint_y=0.1
        )
        layout.add_widget(titulo)
        
        # ScrollView con productos
        scroll = ScrollView(size_hint_y=0.8)
        grid_productos = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        grid_productos.bind(minimum_height=grid_productos.setter('height'))
        
        # Filtrar productos por categoría
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
        
        # Botón volver
        btn_volver = Button(
            text='← VOLVER A CATEGORÍAS',
            size_hint_y=0.1,
            background_color=(0.7, 0.2, 0.2, 1)
        )
        btn_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'categorias'))
        layout.add_widget(btn_volver)
        
        self.add_widget(layout)


class RestauranteApp(App):
    """Aplicación principal del menú de restaurante"""
    
    def build(self):
        # Cargar datos del JSON
        with open('menu.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
        productos = datos['productos']
        
        # Crear Screen Manager
        sm = ScreenManager()
        
        # Agregar pantallas
        sm.add_widget(PantallaInicial(name='inicio'))
        sm.add_widget(PantallaCategorias(productos, name='categorias'))
        sm.add_widget(PantallaProductos(productos, name='productos'))
        
        return sm


if __name__ == '__main__':
    app = RestauranteApp()
    app.run()
