from Scripts.Tools.Action import Action
from Scripts.Graphic.Image import Image
from Scripts.Button.MouseManager import MouseManager
from typing import Callable
from Scripts.Locals import ButtonEvent
from pygame import Rect, Vector2
from Scripts.GameObject.Component import Component


class Button(Component):
    '''
    實現按鈕事件，並提供註冊觸發事件時呼叫某些方法的功能。

    與MouseManager溝通的組件(Component)

    屬性:
        -button_size:Vector2
        -button_center:Vector2
    '''

    def __init__(self) -> None:
        super().__init__()
        self.button_size: Vector2 = None
        self.button_center: Vector2 = None

        self.button_events: dict[ButtonEvent, Action] = {}
        self.mouse_over = False
        self.mouse_pressed = False

    # region setter
    def set_button_size(self, button_size: Vector2):
        self.button_size = Vector2(button_size)
        if not self.button_center:
            self.button_center = self.button_size/2

    def set_button_center(self, button_center: Vector2):
        self.button_size = Vector2(button_center)
    # endregion

    def awake(self):
        MouseManager.attach(self)

    def on_destroy(self):
        if self.mouse_over:
            self.notify(ButtonEvent.exit)
        MouseManager.detach(self)
        self.button_events.clear()

    def check(self, mouse_pos: Vector2, mouse_pressed: bool):
        """根據滑鼠輸入出發按鈕事件"""
        button_rect = Rect(
            self.position.xy-self.button_center, self.button_size)
        mouse_over = button_rect.collidepoint(mouse_pos)

        if mouse_over:
            if not(self.mouse_pressed) and mouse_pressed:
                self.down()
            if self.mouse_pressed and mouse_pressed:
                self.drag()
            if self.mouse_pressed and not(mouse_pressed):
                self.up()
        if not(self.mouse_over) and mouse_over:
            self.enter()
        if self.mouse_over and mouse_over:
            self.over()
        if self.mouse_over and not(mouse_over):
            self.exit()

        self.mouse_over = mouse_over
        self.mouse_pressed = mouse_pressed

        return mouse_over

    def down(self):
        self.notify(ButtonEvent.down)
    def drag(self):
        self.notify(ButtonEvent.drag)
    def up(self):
        self.notify(ButtonEvent.up)
    def enter(self):
        self.notify(ButtonEvent.enter)
    def over(self):
        self.notify(ButtonEvent.over)
    def exit(self):
        self.notify(ButtonEvent.exit)


    def get_button_event(self,button_event: ButtonEvent):
        if not button_event in self.button_events:
            self.button_events[button_event] = Action()
        return self.button_events[button_event]

    def notify(self, button_event: ButtonEvent):
        '''
        通知所有註冊了該按鈕事件的方法
        '''
        if not button_event in self.button_events:
            return
        self.button_events[button_event].notify()
