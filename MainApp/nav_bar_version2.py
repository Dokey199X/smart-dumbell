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
from kivy.properties import NumericProperty
import firebase_admin
from firebase_admin import credentials, db
import datetime
import uuid
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt


Window.size = (350, 600)
Builder.load_file('tech.kv')
exercise = ""
totalCount = 0
userReference = ""

class LoginScreen(Screen):
    def login(self, username, password):
        global userReference
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
            userReference = self.Username
            self.login_check = True
            self.manager.current = 'navigate'
            print(userReference)
        else:
            print("user no longer exists")

    def close_username_dialog(self, obj):
        self.dialog.dismiss()

    def username_changer(self):
        if self.login_check:
            self.get_screen('navigate')

class SignupScreen(Screen):
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
            requests.patch(url="https://login-c2a18-default-rtdb.asia-southeast1.firebasedatabase.app/.json",
                           json=to_database)
            self.manager.current = 'login'

    def close_username_dialog(self, obj):
        self.dialog.dismiss()
class BottomNavigation(Screen):
    pass
class TrainingScreen(Screen):
    pass
class ToneupScreen(Screen):
    def on_enter(self):
        global exercise
        exercise = 'Toneup'

    """def on_enter(self):
        self.ser = serial.Serial('COM3', 9600)
        self.ser.write(b'Tone-up\n')
        self.ser.close()"""

class FemToneupScreen(Screen):
    pass
class MaleToneupScreen(Screen):
    pass
class BulkupScreen(Screen):
    def on_enter(self):
        global exercise
        exercise = 'Bulkup'
    """def on_enter(self):
        self.ser = serial.Serial('COM3', 9600)
        self.ser.write(b'Bulk-up\n')
        self.ser.close()"""

class FemBulkupScreen(Screen):
    pass
class MaleBulkupScreen(Screen):
    pass
class WarmupScreen(Screen):
    def on_enter(self):
        self.countdown = 1
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
        self.countdown = 1
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
    def on_enter(self, *args):
        try:
            self.ser = serial.Serial('COM5', 9600)
            Clock.schedule_interval(self.update, 0.1)
        except serial.SerialException as e:
            print(f"Failed to open serial port: {e}")

    def update(self, dt):
        global totalCount
        try:
            data = self.ser.readline().decode().strip()
            if data.startswith('count:'):
                self.count = int(data.split(':')[1])
                self.ids.count_label1.text = str(self.count)

                if(self.count >= 15):
                    totalCount += self.count
                    self.ser.close()
                    self.manager.current = 'rest'
                #self.manager.current = 'rest'
        except serial.SerialException as e:
            print(f"Serial error: {e}")

    def count_stop(self):
        global totalCount
        totalCount += self.count
        self.ser.close()
        self.manager.current = 'congrats'

class SecondWorkoutScreen(Screen):
    def on_enter(self, *args):
        try:
            self.ser = serial.Serial('COM5', 9600)
            Clock.schedule_interval(self.update, 0.1)
        except serial.SerialException as e:
            print(f"Failed to open serial port: {e}")

    def update(self, dt):
        global totalCount
        try:
            data = self.ser.readline().decode().strip()
            if data.startswith('count:'):
                self.count = int(data.split(':')[1])
                self.ids.count_label2.text = str(self.count)

                if(self.count >= 15):
                    totalCount += self.count
                    self.ser.close()
                    self.manager.current = 'congrats'
                #self.manager.current = 'rest'
        except serial.SerialException as e:
            print(f"Serial error: {e}")

    def count_stop(self):
        global totalCount
        totalCount += self.count
        self.ser.close()
        self.manager.current = 'congrats'

class CongratulationsScreen(Screen):
    def save_records(self, *args):
        global exercise, totalCount, userReference

        # Construct the record to save
        record = {
            'Username': userReference,
            'Date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'Total': totalCount
        }

        # Send a POST request to Firebase Realtime Database REST API to save the record
        url = 'https://test-60202-default-rtdb.asia-southeast1.firebasedatabase.app/' + exercise + '.json'
        response = requests.post(url, data=json.dumps(record))

        # Check if the request was successful
        if response.status_code == 200:
            # Reset the total count and navigate to the next screen
            totalCount = 0
            self.manager.current = 'navigate'
        else:
            # Handle the error if the request was not successful
            print('Failed to save record:', response.text)

class ResultsScreen(Screen):
    pass

class ToneupChartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chart = None

    def on_enter(self):
        global userReference
        url = 'https://test-60202-default-rtdb.asia-southeast1.firebasedatabase.app/Toneup.json'
        params = {"orderBy": "\"Username\"", "equalTo": "\"{}\"".format(userReference)}
        response = requests.get(url, params=params)
        data = response.json()

        record = {}
        for key, value in data.items():
            date = value['Date']
            total_reps = value['Total']
            if date not in record:
                record[date] = total_reps
            else:
                record[date] += total_reps

        fig, ax = plt.subplots()
        ax.bar(record.keys(), record.values())
        ax.set_title('TONE-UP PROGRESS',  fontweight='bold', fontname='Century Gothic',fontsize=18)
        ax.tick_params(axis='x', which='major', labelsize=5)
        plt.xticks(rotation=90)

        self.chart = FigureCanvasKivyAgg(fig)
        self.add_widget(self.chart)

    def go_back(self):
        self.manager.current = 'navigate'

class BulkupChartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chart = None

    def on_enter(self):
        global userReference
        url = 'https://test-60202-default-rtdb.asia-southeast1.firebasedatabase.app/Bulkup.json'
        params = {"orderBy": "\"Username\"", "equalTo": "\"{}\"".format(userReference)}
        response = requests.get(url, params=params)
        data = response.json()

        record = {}
        for key, value in data.items():
            date = value['Date']
            total_reps = value['Total']
            if date not in record:
                record[date] = total_reps
            else:
                record[date] += total_reps

        fig, ax = plt.subplots()
        ax.bar(record.keys(), record.values())
        ax.set_title('TONE-UP PROGRESS', fontweight='bold', fontname='Century Gothic', fontsize=18)
        ax.tick_params(axis='x', which='major', labelsize=5)
        plt.xticks(rotation=90)

        self.chart = FigureCanvasKivyAgg(fig)
        self.add_widget(self.chart)

    def go_back(self):
        self.manager.current = 'navigate'

class MyScreenManager(ScreenManager):
    pass

class MyApp(MDApp):
    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    MyApp().run()