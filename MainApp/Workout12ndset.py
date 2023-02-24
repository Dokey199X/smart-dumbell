from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import serial
from kivymd.app import MDApp
from kivy.core.window import Window

Window.size = (350, 600)
Builder.load_string('''
<CountScreen>:
    Image:
        source:'dumbbellbkg.png'
    MDLabel:
        text: "WORKOUT 1"
        pos_hint: {"center_y": .68}
        halign: "center"
        font_name: "KivyMD/kivymd/fonts/Bebas-Regular.ttf"
        font_size: "40sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    MDLabel:
        text: "2ND SET"
        pos_hint: {"center_y": .60}
        halign: "center"
        font_name: "KivyMD/kivymd/fonts/Bebas-Regular.ttf"
        font_size: "20sp"
        theme_text_color: "Custom"
        theme_color: 60/255, 43/255, 117/255, 1
    MDLabel:
        id: count_label
        text: 'Count: 0'
        halign: 'center'
        font_style: 'H3'
        pos_hint: {'center_y': 0.5}
    
    Button:
        text: "BACK"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"left":1}
        #on_press:
            #root.manager.current = 'Recodumbworkscreen'
            #root.manager.transition.direction ='right'
    Button:
        text: "Next"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"right":1}
        #on_press:
            #root.manager.current = 'workout12ndsetscreen'
            #root.manager.transition.direction ='left'
''')


class CountScreen(Screen):
    pass

class CountApp(MDApp):
    def build(self):
        self.ser = serial.Serial('COM6', 9600)

        self.sm = ScreenManager()
        self.sm.add_widget(CountScreen(name='count'))

        Clock.schedule_interval(self.update, 0.1)

        return self.sm

    def update(self, dt):
        data = self.ser.readline().decode().strip()

        if data.startswith('count:'):
            count = int(data.split(':')[1])
            count_label = self.sm.get_screen('count').ids.count_label
            count_label.text = f'Count: {count}'

if __name__ == '__main__':
    CountApp().run()
