import psycopg2
from psycopg2 import sql
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

# Configurações do banco de dados
DB_CONFIG = {
    'dbname': 'servicos',
    'user': 'GABRIEL',
    'password': '123456',
    'host': '192.168.10.52',
    'port': '5432'
}

# Funções para acessar o banco de dados
def get_service_orders():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM ordens")
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return orders

def validate_user(username, password):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    query = sql.SQL("SELECT * FROM usuarios WHERE id_usuario = %s AND senha = %s")
    cur.execute(query, (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

# Telas do Kivy
class LoginScreen(Screen):
    def do_login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text
        if validate_user(username, password):
            self.manager.current = 'main'
        else:
            self.ids.message_label.text = "Usuário ou senha inválidos"

class MainScreen(Screen):
    def go_to_orders(self):
        self.manager.current = 'orders'
    
    def go_to_register(self):
        self.manager.current = 'register'

class OrdersScreen(Screen):
    def on_pre_enter(self):
        self.ids.orders_list.clear_widgets()
        orders = get_service_orders()
        for order in orders:
            self.ids.orders_list.add_widget(Label(text=str(order)))

class RegisterScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(OrdersScreen(name='orders'))
        sm.add_widget(RegisterScreen(name='register'))
        return sm

if __name__ == '__main__':
    MyApp().run()
