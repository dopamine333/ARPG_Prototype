from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Animation.Animation import Animation
from Scripts.GameObject.Component import Component
from Scripts.Graphic.Render.Render import Render
from Scripts.Graphic.Image import Image


class Animator(Component):
    '''
    播放動畫的組件(Component)

    使用有限狀態機(finite-state machine，FSM)

    可以新增動畫片段，設定切換動畫條件

    向動畫註冊事件。

    屬性:
        -render:Render
        -default_animation: Animation
        -current_animation: Animation
        -animations: list[Animation] 
        -bool_parameters: dict[str,bool]
        -trigger_parameters: dict[str,bool]
    '''

    def __init__(self) -> None:
        super().__init__()
        self.bool_parameters: dict[str, bool] = {}
        self.trigger_parameters: dict[str, bool] = {}
        self.animations: list[Animation] = []
        self.current_animation: Animation = None
        self.default_animation: Animation = None

        self.render: Render = None

    # region setter

    def set_render(self, render: Render):
        self.render = render

    def set_default_animation(self, default_animation: Animation):
        self.default_animation = default_animation
        if not default_animation in self.animations:
            self.add_animation(default_animation)

    # endregion
    def awake(self):
        self.render = self.get_component(Render)
        self.current_animation = self.default_animation

    def start(self):
        self.current_animation.play()

    def add_trigger(self, *parameter_names: str):
        for parameter_name in parameter_names:
            self.trigger_parameters[parameter_name] = False

    def add_bool(self, *parameter_names: str):
        for parameter_name in parameter_names:
            self.bool_parameters[parameter_name] = False

    def set_trigger(self, parameter_name: str):
        self.trigger_parameters[parameter_name] = True

    def set_bool(self, parameter_name: str, value: bool):
        self.bool_parameters[parameter_name] = value

    def add_animation(self, animation: Animation):
        animation.animator = self
        self.animations.append(animation)

    def add_animations(self, *animations: Animation):
        for animation in animations:
            animation.animator = self
            self.animations.append(animation)

    def set_image(self, image: Image):
        self.render.set_image(image)

    def animation_update(self):
        self.current_animation.update()

        for trigger_parameter_name in self.trigger_parameters:
            self.trigger_parameters[trigger_parameter_name] = False

    def get_parameter(self, parameter_name: str):
        if parameter_name in self.trigger_parameters:
            return self.trigger_parameters[parameter_name]
        if parameter_name in self.bool_parameters:
            return self.bool_parameters[parameter_name]
        return None

    def change_animation(self, new_animation: Animation):
        self.current_animation = new_animation
        self.current_animation.play()
