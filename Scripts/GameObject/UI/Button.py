from Scripts.Graph.Image import Image
from Scripts.Managers.MouseManager import MouseManager
from typing import Callable
from Scripts.Locals import ButtonEvent
from pygame import Rect, Vector2
from Scripts.GameObject.UI.UI import UI


class Button(UI):
    def __init__(self, image: Image, button_rect: Rect) -> None:
        super().__init__(image, button_rect.center)
        self.button_rect = button_rect

        self.button_events: dict[ButtonEvent, list[Callable]] = {}

        self.mouse_over = False
        self.mouse_pressed = False

    def start(self):
        MouseManager.Instance().attach(self)

    def end(self):
        MouseManager.Instance().detach(self)

    def check(self, mouse_pos: Vector2, mouse_pressed: bool):
        """
        change button state by mouse input
        """
        mouse_over = self.button_rect.collidepoint(mouse_pos)

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

    def down(self):
        self.notify(ButtonEvent.down)

    def enter(self):
        self.notify(ButtonEvent.enter)

    def exit(self):
        self.notify(ButtonEvent.exit)

    def over(self):
        self.notify(ButtonEvent.over)

    def up(self):
        self.notify(ButtonEvent.up)

    def drag(self):
        self.notify(ButtonEvent.drag)

    def attach(self, button_event: ButtonEvent, func: Callable):
        '''
        Attach a func on a button event.

        if button notify this event,

        the func will be called.
        '''
        if not button_event in self.button_events:
            self.button_events[button_event] = []
        self.button_events[button_event].append(func)

    def detach(self, button_event: ButtonEvent, func: Callable):
        '''
        Detach a func from the button event.
        '''
        if not button_event in self.button_events:
            raise Exception("detach the unkwon event!")
        if not func in self.button_events[button_event]:
            raise Exception("detach the unkwon func!")

        self.button_events[button_event].remove(func)

    def notify(self, button_event: ButtonEvent):
        '''
        Notify all func which is on the button event.
        '''
        if not button_event in self.button_events:
            return
        for func in self.button_events[button_event]:
            func()
