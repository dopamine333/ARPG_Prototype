from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # The TYPE_CHECKING constant is always False at runtime
    # but type-checking tools will evaluate the contents of that block.
    from Scripts.Scene.Scenes.Scene import Scene
    from Scripts.Graph.Render import Render


class SceneChanger:
    def __init__(self) -> None:
        self.current_scene: Scene = None

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, render: Render):
        if self.current_scene:
            self.current_scene.draw(render)

    def change(self, new_scene: Scene):
        if self.current_scene:
            self.current_scene.end()
            self.current_scene.release()
        self.current_scene = new_scene
        self.current_scene.init()
        self.current_scene.start()
