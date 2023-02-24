from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import requests
from kivy.core.window import Window
from kivy.clock import Clock
import serial

Window.size = (350, 600)
Builder.load_file('tech.kv')

class LoginScreen(Screen):

    def signup(self, username, password):

        signupUsername = username
        signupPassword = password
        if signupUsername.split() == [] or signupPassword.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid input', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        if len(signupUsername.split()) > 1:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Username', text='Please enter username without space',
                                   size_hint=(0.7, 0.2), buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            print(signupUsername, signupPassword)
            signup_info = str(
                {f'\"{signupUsername}\":{{"Password":\"{signupPassword}\","Username":\"{signupUsername}\"}}'})
            signup_info = signup_info.replace(".", "-")
            signup_info = signup_info.replace("\'", "")
            to_database = json.loads(signup_info)
            print((to_database))
            requests.patch(url="https://login-c2a18-default-rtdb.asia-southeast1.firebasedatabase.app/.json", json=to_database)
            self.manager.current = 'login'

    def login(self, username, password):
        self.url = "https://login-c2a18-default-rtdb.asia-southeast1.firebasedatabase.app/.json"
        self.auth = '2WnRpXm3ApDyHD2fEtb7OWI3VzvVYmcmkpGDNV1O'

        self.login_check = False
        supported_loginUsername = username.replace('.', '-')
        supported_loginPassword = password.replace('.', '-')
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        usernames = set()
        for key, value in data.items():
            usernames.add(key)
        if supported_loginUsername in usernames and supported_loginPassword == data[supported_loginUsername][
            'Password']:
            self.Username = data[supported_loginUsername]['Username']
            self.login_check = True
            self.manager.current = 'navigate'
        else:
            print("user no longer exists")

    def close_username_dialog(self, obj):
        self.dialog.dismiss()

    def username_changer(self):
        if self.login_check:
            self.get_screen('navigate')

class SignupScreen(Screen):
    pass
class BottomNavigation(Screen):
    pass
class TrainingScreen(Screen):
    pass
class ToneupScreen(Screen):
    def on_enter(self):
        ser = serial.Serial('COM3', 9600)
        ser.write(b'Tone-up\n')

class FemToneupScreen(Screen):
    pass
class MaleToneupScreen(Screen):
    pass
class BulkupScreen(Screen):
    def on_enter(self):
        ser = serial.Serial('COM3', 9600)
        ser.write(b'Bulk-up\n')

class FemBulkupScreen(Screen):
    pass
class MaleBulkupScreen(Screen):
    pass
class WarmupScreen(Screen):
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
            self.manager.current = 'workone'

class RestingScreen(Screen):
    def on_enter(self):
        self.countdown = 30
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def on_leave(self):
        self.timer_event.cancel()

    def update_timer(self, dt):
        self.countdown -= 1
        self.ids.resting_label.text = str(self.countdown)
        if self.countdown <= 0:
            self.timer_event.cancel()
            self.manager.current = 'worktwo'

class FirstWorkoutScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstWorkoutScreen, self).__init__(**kwargs)
        self.ser = serial.Serial('COM3', 9600)

    def on_enter(self):
        Clock.schedule_interval(self.update, 0.1)

    def update(self, dt):
        data = self.ser.readline().decode().strip()

        if data.startswith('count:'):
            count = int(data.split(':')[1])
            self.ids.count_label.text = f'Count: {count}'

class SecondWorkoutScreen(Screen):
    pass
class CongratulationsScreen(Screen):
    pass
class MyScreenManager(ScreenManager):
    pass

class MyApp(MDApp):
    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    MyApp().run()