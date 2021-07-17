from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Animation.Animator import Animator
    from Scripts.Animation.Animation import Animation


class Transition:
    '''
    將要切換成哪個動畫與切換的條件

    屬性:
        -to_animation: Animation
        -conditions: list[str]       
    '''

    def __init__(self,to_animation: Animation,must_play_over:bool=True) -> None:
        self.animator: Animator = None

        self.to_animation: Animation = to_animation

        self.must_play_over = must_play_over
        self.conditions: list[tuple[str,bool]] = []

    def check(self, is_play_over: bool):
        if self.must_play_over:
            if not is_play_over:
                return
        for condition in self.conditions:
            if self.animator.get_parameter(condition[0])!=condition[1]:
                return
        self.animator.change_animation(self.to_animation)

    def add_condition(self, *conditions:  tuple[tuple[str,bool], ...]):
        self.conditions.extend(conditions)
        return self

    def set_to_animation(self, to_animation: Animation):
        self.to_animation = to_animation
