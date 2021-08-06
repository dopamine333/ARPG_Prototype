from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.GameObject.GameObject import GameObject
from Scripts.Scene.SceneManager import SceneManager


class Scene:
    '''
    呼叫場景上所有的遊戲物件(GameObject)更新

    若要新增場景則繼承此類
    '''

    def __init__(self) -> None:
        self.gameobjects: list[GameObject] = []
        self.to_del_gameobjects: list[GameObject] = []
        self.to_add_gameobjects: list[GameObject] = []

    def add_gameobject(self, gameobject: GameObject):
        self.gameobjects.append(gameobject)

    def add_gameobjects(self, *gameobjects: list[GameObject]):
        self.gameobjects.extend(gameobjects)

    def instantiate_gameobject(self, gameobject: GameObject):
        self.to_add_gameobjects.append(gameobject)
        gameobject.start()

    def destroy_gameobject(self, gameobject: GameObject):
        gameobject.end()
        self.to_del_gameobjects.append(gameobject)

    def scene_start(self):
        '''在start前執行'''
        pass

    def scene_update(self):
        '''在update前執行'''
        pass

    def scene_end(self):
        '''在end後執行'''
        pass

    def start(self):
        for gameobject in self.gameobjects:
            gameobject.start()

    def end(self):
        for gameobject in self.gameobjects:
            gameobject.end()

    def update(self):
        if len(self.to_add_gameobjects)>0:
            self.gameobjects.extend(self.to_add_gameobjects)
            self.to_add_gameobjects.clear()

        for gameobject in self.gameobjects:
            gameobject.update()
        for del_gameobject in self.to_del_gameobjects:
            self.gameobjects.remove(del_gameobject)
        self.to_del_gameobjects.clear()

    def change_scene(self, new_scene_name: type[Scene]):
        SceneManager.change(new_scene_name())
