from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.app import MDApp

Builder.load_file('myy.kv')

class MainScreen(Screen):
    pass

class LoginScreen(Screen):
    def do_login(self, username, password):
        if username == 'myusername' and password == 'mypassword':
            self.manager.current = 'dashboard'
        else:
            # Display an error message
            print('Incorrect username or password')

class DashboardScreen(Screen):
    pass

class TimerScreen(Screen):
    def on_enter(self):
        self.countdown = 10
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def on_leave(self):
        self.timer_event.cancel()

    def update_timer(self, dt):
        self.countdown -= 1
        self.ids.timer_label.text = str(self.countdown)
        if self.countdown <= 0:
            self.timer_event.cancel()
            self.manager.current = 'dashboard'

class MyScreenManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    MyApp().run()
