from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.GameObject.GameObject import GameObject
from Scripts.Scene.SceneManager import SceneManager
from Scripts.Time.Invoker import Invoker


class Scene:
    '''
    呼叫場景上所有的遊戲物件(GameObject)更新

    若要新增場景則繼承此類
    '''

    def __init__(self) -> None:
        self.gameobjects: list[GameObject] = []
        self.to_destroy_gameobjects: list[GameObject] = []
        self.to_instantiate_gameobjects: list[GameObject] = []

    def instantiate(self, *gameobjects: GameObject):
        for gameobject in gameobjects:
            self.to_instantiate_gameobjects.append(gameobject)
            gameobject.awake()

    def is_exist(self, gameobject: GameObject):
        return gameobject in self.gameobjects and gameobject not in self.to_destroy_gameobjects

    def destroy(self, gameobject: GameObject):
        if not self.is_exist(gameobject):
            raise Exception(f"SceneError: destroy a not exist gameobject")
        self.to_destroy_gameobjects.append(gameobject)

    # region gameloop
    def on_load(self):
        pass

    def on_instantiate(self):
        if len(self.to_instantiate_gameobjects) == 0:
            return
        for gameobject in self.to_instantiate_gameobjects:
            self.gameobjects.append(gameobject)
            gameobject.start()
        self.to_instantiate_gameobjects.clear()

    def physics_update(self):
        for gameobject in self.gameobjects:
            gameobject.physics_update()

    def update(self):
        for gameobject in self.gameobjects:
            gameobject.update()
        Invoker.trigger()
        for gameobject in self.gameobjects:
            gameobject.animation_update()
        for gameobject in self.gameobjects:
            gameobject.late_update()

    def on_will_render_object(self):
        for gameobject in self.gameobjects:
            gameobject.on_will_render_object()

    def on_release(self):
        for gameobject in self.gameobjects:
            if gameobject not in self.to_destroy_gameobjects:
                self.to_destroy_gameobjects.append(gameobject)

    def on_destroy(self):
        if len(self.to_destroy_gameobjects) == 0:
            return
        for gameobject in self.to_destroy_gameobjects:
            self.gameobjects.remove(gameobject)
            gameobject.on_destroy()
        self.to_destroy_gameobjects.clear()

    # endregion

    def change_scene(self, new_scene_name: type[Scene]):
        SceneManager.change_scene(new_scene_name())
