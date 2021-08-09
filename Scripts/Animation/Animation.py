from __future__ import annotations

from typing import Callable
from pygame import Rect, Surface, Vector2
import pygame

from Scripts.Graphic.Image import Image

from Scripts.Animation.Animator import Animator
from Scripts.Animation.Transition import Transition

from Scripts.Locals import PlayMode

from Scripts.Tools.Action import Action

class Animation:
    '''
    一個動畫片段

    可以註冊動畫事件，設定切換動畫，不同的播放模式

    屬性:
        -clip: list[Image]
        -animation_events: dict[int, list[Callable]]
        -transitions: list[Transition]
        -length: int
        -play_mode: PlayMode = PlayMode.once
    '''

    def __init__(self) -> None:
        self.clip: list[Image] = []
        self.animation_events: dict[int, Action] = {}
        self.length = 1
        self.frame = 0
        self.animator: Animator = None
        self.transitions: list[Transition] = []

        self.is_playing = False
        self.speed = 1
        self.play_mode = PlayMode.once

    def set_speed(self, speed: float):
        self.speed = speed

    def update(self):
        '''更新動畫'''
        # 更新播放幀
        if self.is_playing:
            # 撥放一次即暫停
            if self.play_mode == PlayMode.once:
                self.frame += self.speed
                if self.frame >= self.length:
                    self.frame = self.length-1
                    self.is_playing = False

            elif self.play_mode == PlayMode.loop:
                # 重複循環
                self.frame = (self.frame+self.speed) % self.length

            elif self.play_mode == PlayMode.pingpong:
                # 來回反覆
                if self.speed > 0:
                    self.frame = self.frame+self.speed
                    if self.frame >= self.length:
                        self.frame = self.length-1
                        self.speed *= -1
                else:
                    self.frame = self.frame+self.speed
                    if self.frame <= 0:
                        self.frame = 1
                        self.speed *= -1
        int_frame = int(self.frame)

        # 設定圖片
        if self.is_playing:
            self.animator.set_image(self.clip[int_frame])
        # 通知動畫事件
        if self.frame in self.animation_events:
            self.animation_events[self.frame].notify()
        # 檢查是否要切換動畫
        for transition in self.transitions:
            transition.check(int_frame == self.length-1)

    def play(self):
        '''開始撥放'''
        self.frame = 0
        self.is_playing = True
        self.animator.set_image(self.clip[int(self.frame)])

    def set_play_mode(self, play_mode: PlayMode):
        self.play_mode = play_mode

    def add_transition(self, to_animation: Animation, must_play_over: bool = True, *conditions:  tuple[tuple[str, bool], ...]):
        '''
        創建一個動畫轉換 可添加條件
        to_animation : 目標動畫
        must_play_over : 一定要播完才能轉換動畫嗎
        conditions : (參數名稱 , 條件值) 
        '''
        transition = Transition(to_animation, must_play_over)
        if len(conditions) != 0:
            transition.add_condition(*conditions)
        transition.animator = self.animator
        self.transitions.append(transition)

    def use_sprite_sheet(self, sprite_sheet: Surface, start_left_top: Vector2, size: Vector2, center: Vector2, lenght: int):
        '''使用精靈圖表(sprite_sheet)設定動畫片段'''
        self.set_clip(self.generate_clip_use_sprite_sheet(
            sprite_sheet, start_left_top, size, center, lenght))

    @staticmethod
    def generate_clip_use_sprite_sheet(sprite_sheet: Surface, start_left_top: Vector2, size: Vector2, center: Vector2, lenght: int):
        '''使用精靈圖表(sprite_sheet)生成動畫片段'''
        clip: list[Image] = []
        size = Vector2(size)
        source_rect = Rect(start_left_top, size)
        for _ in range(lenght):
            source = Surface(size, pygame.SRCALPHA)
            source.blit(sprite_sheet, (0, 0), source_rect)
            clip.append(Image(source, center))

            source_rect.x += size.x
        return clip

    def set_clip(self, clip: list[Image]):
        '''設定動畫片段'''
        self.clip = clip
        self.length = len(clip)

    def get_frame_event(self, frame: int):
        if not frame in self.animation_events:
            self.animation_events[frame] = Action()
        return self.animation_events[frame]

