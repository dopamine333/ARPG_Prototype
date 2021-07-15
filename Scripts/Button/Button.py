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

        self.button_events: dict[ButtonEvent, list[Callable]] = {}
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

    def start(self):
        MouseManager.attach(self)

    def end(self):
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
                self.notify(ButtonEvent.down)
            if self.mouse_pressed and mouse_pressed:
                self.notify(ButtonEvent.drag)
            if self.mouse_pressed and not(mouse_pressed):
                self.notify(ButtonEvent.up)
        if not(self.mouse_over) and mouse_over:
            self.notify(ButtonEvent.enter)
        if self.mouse_over and mouse_over:
            self.notify(ButtonEvent.over)
        if self.mouse_over and not(mouse_over):
            self.notify(ButtonEvent.exit)

        self.mouse_over = mouse_over
        self.mouse_pressed = mouse_pressed

        return mouse_over

    def attach(self, button_event: ButtonEvent, func: Callable):
        '''
        註冊觸發按鈕事件時想被通知的方法
        '''
        if not button_event in self.button_events:
            self.button_events[button_event] = []
        self.button_events[button_event].append(func)

    def detach(self, button_event: ButtonEvent, func: Callable):
        '''
        取消註冊觸發按鈕事件時想被通知的方法
        '''
        if not button_event in self.button_events:
            raise Exception("detach the unkwon event!")
        if not func in self.button_events[button_event]:
            raise Exception("detach the unkwon func!")

        self.button_events[button_event].remove(func)

    def notify(self, button_event: ButtonEvent):
        '''
        通知所有註冊了該按鈕事件的方法
        '''
        if not button_event in self.button_events:
            return
        for func in self.button_events[button_event]:
            func()
