
from collections import defaultdict
from typing import Callable
from pygame import Rect, Surface, Vector2
import pygame
from Scripts.Graphic.Image import Image
from Scripts.Animation.Animator import Animator
from Scripts.Animation.Transition import Transition
from Scripts.Locals import PlayMode


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
        self.animation_events: dict[int, list[Callable[[]]]] = {}
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
            self.notify(int_frame)
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

    def add_transition(self, transition: Transition):
        transition.animator = self.animator
        self.transitions.append(transition)

    def use_sprite_sheet(self, sprite_sheet: Surface, start_left_top: Vector2, size: Vector2, center: Vector2, lenght: int):
        '''使用精靈圖表(sprite_sheet)設定動畫片段'''
        self.length = lenght
        size=Vector2(size)
        source_rect = Rect(start_left_top, size)
        for _ in range(lenght):
            source = Surface(size,pygame.SRCALPHA)
            source.blit(sprite_sheet, (0, 0), source_rect)
            self.clip.append(Image(source, center))

            source_rect.x += size.x

    def set_clip(self, clip: list[Image]):
        '''設定動畫片段'''
        self.clip = clip
        self.length = len(clip)

    def attach(self, frame: int, func: Callable):
        '''
        註冊撥放到該幀時想被通知的方法
        '''
        if not frame in self.animation_events:
            self.animation_events[frame] = []
        self.animation_events[frame].append(func)

    def detach(self, frame: int, func: Callable):
        '''
        取消註冊撥放到該幀時想被通知的方法
        '''
        if not frame in self.animation_events:
            raise Exception("detach the unkwon event!")
        if not func in self.animation_events[frame]:
            raise Exception("detach the unkwon func!")

        self.animation_events[frame].remove(func)

    def notify(self, frame: int):
        '''呼叫所有註冊到這幀的方法'''
        for event in self.animation_events[frame]:
            event()