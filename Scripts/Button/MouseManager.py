from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Button.Button import Button

from pygame.cursors import Cursor
from Scripts.Graphic.Image import Image
from pygame import Vector2, mouse
from Scripts.Locals import ButtonEvent, CursorState
from Scripts.Tools.Singleton import Singleton
from pygame.image import load


class MouseManager:
    '''
    根據狀態切換鼠標圖案

    觸發按鈕事件
    '''

    buttons: list[Button] = []
    cursor_state = CursorState.normal
    cursor_images: dict[CursorState, Image] = {}
    invisible_timer = 0
    invisible_time = 3

    @staticmethod
    def init():
        # FIXME 載入滑鼠圖片
        MouseManager.cursor_images = {
            CursorState.normal: Image(
                load(r"Arts\Cursors\normal_cursor.png").convert_alpha(), (10, 10)
            ),
            CursorState.button: Image(
                load(r"Arts\Cursors\button_cursor.png").convert_alpha(), (28.5, 8.3)
            )
        }
        MouseManager.mouse_exit_buttom()

    @staticmethod
    def attach(button: Button):
        '''註冊按鈕(Button)'''
        MouseManager.buttons.append(button)
        button.get_button_event(ButtonEvent.enter) + MouseManager.mouse_enter_buttom
        button.get_button_event(ButtonEvent.exit) + MouseManager.mouse_exit_buttom

    @staticmethod
    def detach(button: Button):
        '''取消註冊按鈕(Button)'''
        if button in MouseManager.buttons:
            MouseManager.buttons.remove(button)
        button.get_button_event(ButtonEvent.enter) - MouseManager.mouse_enter_buttom
        button.get_button_event(ButtonEvent.exit) - MouseManager.mouse_exit_buttom

    @staticmethod
    def update():
        '''觸發按鈕事件'''
        mouse_pos = mouse.get_pos()
        mouse_pressed = mouse.get_pressed()[0]
        for button in MouseManager.buttons:
            if button.check(mouse_pos, mouse_pressed):
                break
        '''#一段時間不動 滑鼠隱形
        if mouse.get_rel()==(0,0):
            if MouseManager.invisible_timer+MouseManager.invisible_time<time():
                mouse.set_visible(False)
                MouseManager.invisible_timer=time()
        else:
            mouse.set_visible(True)'''

    @staticmethod
    def mouse_enter_buttom():
        # 切換鼠標圖示
        MouseManager.cursor_state = CursorState.button
        image = MouseManager.cursor_images[MouseManager.cursor_state]
        mouse.set_cursor(image.get_int_center(), image.source)

    @staticmethod
    def mouse_exit_buttom():
        # 切換鼠標圖示
        MouseManager.cursor_state = CursorState.normal
        image = MouseManager.cursor_images[MouseManager.cursor_state]
        mouse.set_cursor(image.get_int_center(), image.source)
