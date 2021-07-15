from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # The TYPE_CHECKING constant is always False at runtime
    # but type-checking tools will evaluate the contents of that block.
    from Scripts.Scene.Scenes.Scene import Scene


class SceneManager:
    '''
    切換場景(Scene)

    呼叫當前場景更新
    '''
    current_scene: Scene = None

    @staticmethod
    def update():
        if SceneManager.current_scene:
            SceneManager.current_scene.scene_update()
            SceneManager.current_scene.update()

    @staticmethod
    def change(new_scene: Scene):
        if SceneManager.current_scene:
            SceneManager.current_scene.end()
            SceneManager.current_scene.scene_end()
        SceneManager.current_scene = new_scene
        SceneManager.current_scene.scene_start()
        SceneManager.current_scene.start()
