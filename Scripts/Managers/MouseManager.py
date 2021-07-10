from __future__ import annotations
from typing import TYPE_CHECKING

from pygame.cursors import Cursor
if TYPE_CHECKING:
    from Scripts.GameObject.UI.Button import Button
from Scripts.Graph.Image import Image
from pygame import Vector2, mouse
from Scripts.Locals import ButtonEvent, CursorState
from Scripts.Tools.Singleton import Singleton
from pygame.image import load


class MouseManager(Singleton):
    '''
    A manager of mouse,

    can swicth cursor image by mouse state and

    trigger buttons which was attached
    '''
    def __init__(self) -> None:
        self.buttons: list[Button] = []
        self.cursor_state = CursorState.normal
        self.cursor_images: dict[CursorState, Image] = {
            CursorState.normal: Image(load(r"Arts\Cursors\normal_cursor.png").convert_alpha(), (10, 10)),
            CursorState.button: Image(
                load(r"Arts\Cursors\button_cursor.png").convert_alpha(), (28.5, 8.3))
        }

    def attach(self, button: Button):
        self.buttons.append(button)
        button.attach(ButtonEvent.over, self.mouse_over_buttom)

    def detach(self, button: Button):
        if button in self.buttons:
            self.buttons.remove(button)
        button.detach(ButtonEvent.over, self.mouse_over_buttom)

    def update(self):
        mouse_pos = mouse.get_pos()
        mouse_pressed = mouse.get_pressed()[0]
        for button in self.buttons:
            button.check(mouse_pos, mouse_pressed)
        #update_cursor    
        image = self.cursor_images[self.cursor_state]
        mouse.set_cursor(image.get_int_center(), image.source)

        self.cursor_state = CursorState.normal
        

    def mouse_over_buttom(self):
        self.cursor_state = CursorState.button
