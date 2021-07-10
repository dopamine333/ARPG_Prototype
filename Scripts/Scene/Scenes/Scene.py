from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # The TYPE_CHECKING constant is always False at runtime
    # but type-checking tools will evaluate the contents of that block.
    from Scripts.Graph.Camera import Camera
    from Scripts.Scene.SceneChanger import SceneChanger
    from Scripts.GameObject.GameObject import GameObject


class Scene:
    def __init__(self, scene_changer: SceneChanger) -> None:
        self.scene_changer = scene_changer
        self.gameobjects: list[GameObject] = []

    def add_gameobjects(self, *gameobjects: list[GameObject]):
        self.gameobjects.extend(gameobjects)

    def remove_gameobject(self, gameobject: GameObject):
        self.gameobjects.remove(gameobject)

    def init(self):
        pass

    def release(self):
        pass

    def start(self):
        for gameobject in self.gameobjects:
            gameobject.start()

    def end(self):
        for gameobject in self.gameobjects:
            gameobject.end()

    def update(self):
        for gameobject in self.gameobjects:
            gameobject.update()

    def draw(self, camera: Camera):
        for gameobject in self.gameobjects:
            gameobject.draw(camera)

    def change_scene(self, new_scene_name: type[Scene]):
        self.scene_changer.change(new_scene_name(self.scene_changer))
