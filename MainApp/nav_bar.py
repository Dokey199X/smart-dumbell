from kivymd.app import MDApp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import requests
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.factory import Factory as F
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, NumericProperty



Window.size = (350, 600)
Builder.load_string('''
<Timer>:
    orientation: 'vertical'
    MDLabel:
        text: '{:.2f} remaining / {:.2f}'.format(root.remaining, root.total)
        pos_hint: {"center_y": .60}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 

    MDRaisedButton:
        text: 'Start'
        pos_hint: {"center_x": .5, "center_y": .35}
        halign: "center"
        on_press: root.start()
        disabled: root.active
''')

class Timer(F.BoxLayout):
    active = F.BooleanProperty(False)
    complete = F.BooleanProperty(False)

    # Total time, and time remaining (in seconds)
    total = F.NumericProperty(0)
    remaining = F.NumericProperty(0)

    def __init__(self, **kwargs):
        super(Timer, self).__init__(**kwargs)
        App.get_running_app().add_timer(self)
        self.remaining = self.total

    def set_total(self, total):
        self.stop()
        self.total = self.remaining = total

    def start(self):
        if self.total:
            self.angle = 0
            self.active = True
            self.complete = False

    def stop(self):
        self.active = self.complete = False
        self.remaining = self.total

    # Called by App every 0.1 seconds (ish)
    def _tick(self, dt):
        if not self.active:
            return
        if self.remaining <= dt:
            self.stop()
            self.complete = True
        else:
            self.remaining -= dt

kv = '''
ScreenManager:
    LoginScreen:
    SignupScreen:
    BottomNavigation:
    
<LoginScreen>:
    name:'loginscreen'
    Image:
        source: "dumbbellbkg.png"
    MDLabel:
        text: "Log In"
        pos_hint: {"center_y": .58}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: root.height / 10
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDTextField:  
        id:login_username
        pos_hint: {"center_x": .5, "center_y": .48}
        size_hint : (0.85,None)
        hint_text: 'Username'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
        required: True
        mode: "rectangle"
    MDTextField:
        id:login_password
        password: True
        pos_hint: {"center_x": .5, "center_y": .35}
        size_hint : (0.85,None)
        hint_text: 'Password'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
        required: True
        mode: "rectangle"
    MDRaisedButton:
        text:'Login'
        font_name: "CenturyGothic.ttf"
        font_size: "20sp"
        size_hint: .5, .08
        pos_hint: {"center_x": .5, "center_y": .2}
        md_bg_color: 0, 0, 0.5, 1 
        on_press:
            app.login()
            app.username_changer() 
    MDTextButton:
        text: 'Create an account'
        font_name: "CenturyGothic.ttf"
        theme_text_color: "Custom"
        text_color: 0, 0, 1, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press:
            root.manager.current = 'signupscreen'
            root.manager.transition.direction = 'up'

<SignupScreen>:
    name:'signupscreen'
    Image:
        source: "logo.jpg"
        pos_hint: {"y": .25}
    MDLabel:
        text:'Sign up'
        font_name:"Bebas-Regular.ttf"
        font_size: root.height / 10
        halign:'center'
        pos_hint: {'center_y':0.58}
    MDTextField:
        id:signup_username
        pos_hint: {"center_x": .5, "center_y": .48}
        size_hint : (0.85,None)
        hint_text: 'Username'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
        required: True
        mode: "rectangle"
  
    MDTextField:
        id:signup_password
        password: True
        pos_hint: {"center_x": .5, "center_y": .35}
        size_hint : (0.85,None)
        hint_text: 'Password'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
        required: True
        mode: "rectangle"
    MDRaisedButton:
        text:'Sign up'
        font_name: "CenturyGothic.ttf"
        font_size: "20sp"
        size_hint: .5, .08
        pos_hint: {'center_x':0.5,'center_y':0.2}
        on_press: app.signup()
    MDTextButton:
        text: 'Already have an account'
        font_name: "CenturyGothic.ttf"
        theme_text_color: "Custom"
        text_color: 0, 0, 1, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press:
            root.manager.current = 'loginscreen'
            root.manager.transition.direction = 'down'

<BottomNavigation>:
    name:'bottomnavigation'
    BoxLayout:
        orientation:'vertical'

        MDTopAppBar:
            title: 'Smart Dumbbell'
            md_bg_color: .2, .2, .2, 1
            specific_text_color: 1, 1, 1, 1
        
        MDBottomNavigation:
            panel_color: .2, .2, .2, 1
            
            MDBottomNavigationItem:
                name: 'HomeScreen'
                text: 'Home'
                icon: 'home'
                MDScreen:
                    Button:
                        text: "LOG OUT"
                        size_hint: .25, None
                        height: "60dp"
                        pos_hint: {"left": 1 }
                        on_press:
                            root.manager.current = 'loginscreen'
                            root.manager.transition.direction = 'up'

            MDBottomNavigationItem:
                name: 'Bluetooth'
                text: 'Connect'
                font_size: root.height / 20
                icon: 'bluetooth'
                MDScreen:
                    MDLabel:
                        text:'Bluetooth'
                        font_style:"H2"
                        font_size: root.height / 20

            MDBottomNavigationItem:
                name: 'Workout'
                text: 'Workout'
                font_size: root.height / 20
                icon: 'dumbbell'
                ScreenManager:
                    Training:
                    Gendertoneup:
                    Femaletoneup:
                    Maletoneup:
                    Genderbulkup:
                    Femalebulkup:
                    Malebulkup:
                    Warmup:
                    Workout1:
                    Workout12ndset:
                    Workout2:
                    Workout22ndset:
                    Congrats:

            MDBottomNavigationItem:
                name: 'Record'
                text: 'Record'
                font_size: root.height / 20
                icon: 'chart-line'
                MDScreen:
                    MDLabel:
                        text:'Graph'
                        font_style:"H2"
                        font_size: root.height / 20
            
            MDBottomNavigationItem:
                name: 'Info'
                text: 'About'
                font_size: root.height / 20
                icon: 'information'
                MDScreen:
                    MDLabel:
                        text:'About'
                        font_style:"H2"
                        font_size: root.height / 20
<Training>:
    name:'trainingscreen'
    MDLabel:
        text: "Training Excercise"
        pos_hint: {"center_y": .60}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: root.height / 10
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDRaisedButton:
        text:'Tone-Up'
        font_name: "CenturyGothic.ttf"
        font_size: "20sp"
        text_color: 1, 1, 1, 1
        size_hint: .5, .08
        pos_hint: {"center_x": .5, "center_y": .50}
        md_bg_color: 0, 0, 0.5, 1 
        on_press:
            root.manager.current = 'genderscreentoneup'
            root.manager.transition.direction = 'left'
    MDRaisedButton:
        text:'Bulk-Up'
        font_name: "CenturyGothic.ttf"
        font_size: "20sp"
        text_color: 1, 1, 1, 1
        size_hint: .5, .08
        pos_hint: {"center_x": .5, "center_y": .40} 
        md_bg_color: 0, 0, 0.5, 1   
        on_press:
            root.manager.current = 'genderscreenbulkup'
            root.manager.transition.direction = 'left'

<Gendertoneup>:
    name:'genderscreentoneup'
    MDLabel:
        text: "Gender"
        pos_hint: {"center_y": .60}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: root.height / 10
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDRaisedButton:
        text:'Female'
        font_name: "CenturyGothic.ttf"
        font_size: "20sp"
        text_color: 1, 1, 1, 1
        size_hint: .5, .08
        pos_hint: {"center_x": .5, "center_y": .50}
        md_bg_color: 0, 0, 0.5, 1 
        on_press:
            root.manager.current = 'femalescreen'
            root.manager.transition.direction = 'left'
    MDRaisedButton:
        text:'Male'
        font_name: "CenturyGothic.ttf"
        font_size: "20sp"
        text_color: 1, 1, 1, 1
        size_hint: .5, .08
        pos_hint: {"center_x": .5, "center_y": .40}
        md_bg_color: 0, 0, 0.5, 1  
        on_press:
            root.manager.current = 'malescreen'
            root.manager.transition.direction = 'left'
    Button:
        text: "BACK"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"left":1}
        on_press:
            root.manager.current = 'trainingscreen'
            root.manager.transition.direction ='right'  

<Femaletoneup>:
    name:'femalescreen'
    MDLabel:
        text: "RECOMMENDED TRAINING"
        pos_hint: {"center_y": .65}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    MDLabel:
        text: "FEMALE"
        pos_hint: {"center_y": .58}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1  
    MDLabel:
        text: "Sets: 1-2"
        pos_hint: {"center_y": .50}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDLabel:
        text: "Repetitions: 10-12"
        pos_hint: {"center_y": .46}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDLabel:
        text: "Weights: 1.5kg-5kg"
        pos_hint: {"center_y": .42}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDRaisedButton:
        text: "START"
        pos_hint: {"center_x":.5,"center_y":.3}
        size_hint: .25, None
        height: "60dp"
        on_press:
            root.manager.current = 'warmupscreen'
            root.manager.transition.direction ='left'
    Button:
        text: "BACK"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"left":1}
        on_press:
            root.manager.current = 'genderscreentoneup'
            root.manager.transition.direction ='right'

<Maletoneup>:
    name:'malescreen'
    MDLabel:
        text: "RECOMMENDED TRAINING"
        pos_hint: {"center_y": .65}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    MDLabel:
        text: "MALE"
        pos_hint: {"center_y": .58}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1  
    MDLabel:
        text: "Sets: 1-2"
        pos_hint: {"center_y": .50}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDLabel:
        text: "Repetitions: 12-15"
        pos_hint: {"center_y": .46}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDLabel:
        text: "Weights: 2.5kg-12kg"
        pos_hint: {"center_y": .42}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDRaisedButton:
        text: "START"
        pos_hint: {"center_x":.5,"center_y":.3}
        size_hint: .25, None
        height: "60dp"
        on_press:
            root.manager.current = 'warmupscreen'
            root.manager.transition.direction ='left'
    Button:
        text: "BACK"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"left":1}
        on_press:
            root.manager.current = 'genderscreentoneup'
            root.manager.transition.direction ='right'

<Genderbulkup>:
    name:'genderscreenbulkup'
    MDLabel:
        text: "Gender"
        pos_hint: {"center_y": .60}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDRaisedButton:
        text:'Female'
        font_name: "CenturyGothic.ttf"
        font_size: "20sp"
        text_color: 1, 1, 1, 1
        size_hint: .5, .08
        pos_hint: {"center_x": .5, "center_y": .50}
        md_bg_color: 0, 0, 0.5, 1 
        on_press:
            root.manager.current = 'femalescreenbulkup'
            root.manager.transition.direction = 'left'
    MDRaisedButton:
        text:'Male'
        font_name: "CenturyGothic.ttf"
        font_size: "20sp"
        text_color: 1, 1, 1, 1
        size_hint: .5, .08
        pos_hint: {"center_x": .5, "center_y": .40}
        md_bg_color: 0, 0, 0.5, 1  
        on_press:
            root.manager.current = 'malescreenbulkup'
            root.manager.transition.direction = 'left'
    Button:
        text: "BACK"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"left":1}
        on_press:
            root.manager.current = 'trainingscreen'
            root.manager.transition.direction ='right'  

<Femalebulkup>:
    name:'femalescreenbulkup'
    MDLabel:
        text: "RECOMMENDED TRAINING"
        pos_hint: {"center_y": .65}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    MDLabel:
        text: "FEMALE"
        pos_hint: {"center_y": .58}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1  
    MDLabel:
        text: "Sets: 1-2"
        pos_hint: {"center_y": .50}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDLabel:
        text: "Repetitions: 5-8"
        pos_hint: {"center_y": .46}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDLabel:
        text: "Weights: 1.5kg-12kg"
        pos_hint: {"center_y": .42}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDRaisedButton:
        text: "START"
        pos_hint: {"center_x":.5,"center_y":.3}
        size_hint: .25, None
        height: "60dp"
        on_press:
            root.manager.current = 'warmupscreen'
            root.manager.transition.direction ='left'
    Button:
        text: "BACK"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"left":1}
        on_press:
            root.manager.current = 'genderscreenbulkup'
            root.manager.transition.direction ='right'

<Malebulkup>:
    name:'malescreenbulkup'
    MDLabel:
        text: "RECOMMENDED TRAINING"
        pos_hint: {"center_y": .65}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    MDLabel:
        text: "MALE"
        pos_hint: {"center_y": .58}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1  
    MDLabel:
        text: "Sets: 1-2"
        pos_hint: {"center_y": .50}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDLabel:
        text: "Repetitions: 5-8"
        pos_hint: {"center_y": .46}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDLabel:
        text: "Weights: 2.5kg-22kg"
        pos_hint: {"center_y": .42}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
    MDRaisedButton:
        text: "START"
        pos_hint: {"center_x":.5,"center_y":.3}
        size_hint: .25, None
        height: "60dp"
        on_press:
            root.manager.current = 'warmupscreen'
            root.manager.transition.direction ='left'
    Button:
        text: "BACK"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"left":1}
        on_press:
            root.manager.current = 'genderscreenbulkup'
            root.manager.transition.direction ='right'
<Warmup>:
    name:'warmupscreen'
    orientation: 'vertical'
    #Image:
        #source:'dumbbellbkg.png'
    MDLabel:
        text: "WARM UP"
        pos_hint: {"center_y": .60}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1 
        
    MDRaisedButton:
        text: "Ready"
        pos_hint: {"center_x": .5, "center_y": .35}
        on_press: container.add_widget(F.Timer(total=300))
        
    BoxLayout:
        id: container
        orientation: 'horizontal'
        spacing: 5
            
    Button:
        text: "BACK"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"left":1}
        on_press:
            root.manager.current = 'trainingscreen'
            root.manager.transition.direction ='right'
    Button:
        text: "NEXT"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"right":1}
        on_press:
            root.manager.current = 'workout1screen'
            root.manager.transition.direction ='left'
    
<Workout1>:
    name:'workout1screen'
    MDLabel:
        text: "WORKOUT 1"
        pos_hint: {"center_y": .68}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    MDLabel:
        text: "1ST SET"
        pos_hint: {"center_y": .60}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    MDLabel:
        text: "Counter:<dumbbell>"
        pos_hint: {"center_y": .45, "center_x": .48}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "30sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    MDRaisedButton:
        text: "STOP"
        pos_hint: {"center_x":.5,"center_y":.3}
        size_hint: .25, None
        height: "60dp"
    Button:
        text: "BACK"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"left":1}
        on_press:
            root.manager.current = 'warmupscreen'
            root.manager.transition.direction ='right'
    Button:
        text: "Next"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"right":1}
        on_press:
            root.manager.current = 'workout12ndsetscreen'
            root.manager.transition.direction ='left'
<Workout12ndset>
    name:'workout12ndsetscreen'
    MDLabel:
        text: "WORKOUT 1"
        pos_hint: {"center_y": .68}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    MDLabel:
        text: "2ND SET"
        pos_hint: {"center_y": .60}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    MDLabel:
        text: "Counter:<dumbbell>"
        pos_hint: {"center_y": .45, "center_x": .48}
        halign: "center"
        font_name: "Bebas-Regular.ttf"
        font_size: "30sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    MDRaisedButton:
        text: "STOP"
        pos_hint: {"center_x":.5,"center_y":.3}
        size_hint: .25, None
        height: "60dp"
    Button:
        text: "BACK"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"left":1}
        on_press:
            root.manager.current = 'workout1screen'
            root.manager.transition.direction ='right'
    Button:
        text: "FINISHED"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"right":1}
        on_press:
            root.manager.current = 'Congratscreen'
            root.manager.transition.direction ='left'

<Congrats>:
    name:'Congratscreen'
    MDLabel:
        text: "CONGRATS! YOU PASSED THE TRAINING"
        pos_hint: {"center_y": .50}
        halign: "center"
        font_name: "KivyMD/kivymd/fonts/Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    Button:
        text: "BACK"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"left":1}
        on_press:
            root.manager.current = 'workout12ndsetscreen'
            root.manager.transition.direction ='right'
    Button:
        text: "SAVE"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"right":1}
        #on_press:
            #root.manager.current = 'workout2screen'
            #root.manager.transition.direction ='right'
    
'''
class LoginScreen(Screen):
    pass
class SignupScreen(Screen):
    pass
class BottomNavigation(Screen):
    pass
class Training(Screen):
    pass
class Gendertoneup(Screen):
    pass
class Femaletoneup(Screen):
    pass
class Maletoneup(Screen):
    pass
class Genderbulkup(Screen):
    pass
class Femalebulkup(Screen):
    pass
class Malebulkup(Screen):
    pass
class Warmup(Screen):
    pass
class Warmup2(Screen):
    pass
class Workout1(Screen):
    pass
class Workout2(Screen):
    pass
class Workout12ndset(Screen):
    pass
class Workout22ndset(Screen):
    pass
class Congrats(Screen):
    pass

sm = ScreenManager()
sm.add_widget(BottomNavigation(name = 'bottomnav'))
sm.add_widget(LoginScreen(name = 'loginscreen'))
sm.add_widget(SignupScreen(name = 'signupscreen'))
sm.add_widget(Warmup(name='warmupscreen'))
sm.add_widget(Workout1(name = 'workout1screen'))
sm.add_widget(Workout2(name = 'workout2screen'))
sm.add_widget(Congrats(name = 'Congratsscreen'))


class LoginApp(MDApp):
    def build(self):
        self.strng = Builder.load_string(kv)
        self.url  = "https://login-c2a18-default-rtdb.asia-southeast1.firebasedatabase.app/.json"

        return self.strng

    def signup(self):
        signupUsername = self.strng.get_screen('signupscreen').ids.signup_username.text
        signupPassword = self.strng.get_screen('signupscreen').ids.signup_password.text
        if signupUsername.split() == [] or signupPassword.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text = 'Retry',on_release = self.close_username_dialog)
            self.dialog = MDDialog(title = 'Invalid Input',text = 'Please Enter a valid Input',size_hint = (0.7,0.2),buttons = [cancel_btn_username_dialogue])
            self.dialog.open()
        if len(signupUsername.split())>1:
            cancel_btn_username_dialogue = MDFlatButton(text = 'Retry',on_release = self.close_username_dialog)
            self.dialog = MDDialog(title = 'Invalid Username',text = 'Please enter username without space',size_hint = (0.7,0.2),buttons = [cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            print(signupUsername,signupPassword)
            signup_info = str({f'\"{signupUsername}\":{{"Password":\"{signupPassword}\","Username":\"{signupUsername}\"}}'})
            signup_info = signup_info.replace(".","-")
            signup_info = signup_info.replace("\'","")
            to_database = json.loads(signup_info)
            print((to_database))
            requests.patch(url = self.url,json = to_database)
            self.strng.get_screen('loginscreen').manager.current = 'loginscreen'
    auth = '2WnRpXm3ApDyHD2fEtb7OWI3VzvVYmcmkpGDNV1O'

    def login(self):
        loginUsername = self.strng.get_screen('loginscreen').ids.login_username.text
        loginPassword = self.strng.get_screen('loginscreen').ids.login_password.text

        self.login_check = False
        supported_loginUsername = loginUsername.replace('.','-')
        supported_loginPassword = loginPassword.replace('.','-')
        request  = requests.get(self.url+'?auth='+self.auth)
        data = request.json()
        usernames= set()
        for key,value in data.items():
            usernames.add(key)
        if  supported_loginUsername in usernames and supported_loginPassword == data[supported_loginUsername]['Password']:
            self.Username = data[supported_loginUsername]['Username']
            self.login_check=True
            self.strng.get_screen('bottomnavigation').manager.current = 'bottomnavigation'
        else:
            print("user no longer exists")
    def close_username_dialog(self,obj):
        self.dialog.dismiss()
    def username_changer(self):
        if self.login_check:
            self.strng.get_screen('bottomnavigation')

    
class WarmupApp(MDApp):
    _timers = []
    _clock = None
    
    def build(self):
        return Builder.load_string(kv)

    def add_timer(self, timer):
        self._timers.append(timer)
        if not self._clock:
            self._clock = Clock.schedule_interval(self._progress_timers, 0.1)

    def _progress_timers(self, dt):
        for t in self._timers:
            t._tick(dt)


if __name__ == '__main__':
    LoginApp().run()
    
