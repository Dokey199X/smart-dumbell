from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.app import runTouchApp
from kivy.factory import Factory as F

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

#class TimeApp(Screen):
Window.size = (350, 600)

Builder.load_string('''
<Timer>:
    orientation: 'vertical'
    MDLabel:
        text: '{:.2f} remaining / {:.2f}'.format(root.remaining, root.total)
        pos_hint: {"center_y": .60}
        halign: "center"
        font_name: "Arial"
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

help_str ='''
#:import F kivy.factory.Factory

ScreenManager:
    Warmup:
<Warmup>:
    name:'warmupscreen'
    orientation: 'vertical'
    Image:
        source:'dumbbellbkg.png'
    MDLabel:
        text: "WARM UP"
        pos_hint: {"center_y": .60}
        halign: "center"
        font_name: "Arial"
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
        #on_press:
            #root.manager.current = 'workout2screen'
            #root.manager.transition.direction ='right'
    Button:
        text: "NEXT"
        size_hint: .25, None
        height: "60dp"
        pos_hint: {"right":1}
        #on_press:
            #root.manager.current = 'workout2screen'
            #root.manager.transition.direction ='right'
'''

class Warmup(Screen):
    pass

sm = ScreenManager()
sm.add_widget(Warmup(name='warmupscreen'))

class WarmupApp(MDApp):
    _timers = []
    _clock = None

    def build(self):
        return Builder.load_string(help_str)

    def add_timer(self, timer):
        self._timers.append(timer)
        if not self._clock:
            self._clock = Clock.schedule_interval(self._progress_timers, 0.1)

    def _progress_timers(self, dt):
        for t in self._timers:
            t._tick(dt)

WarmupApp().run()