from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # The TYPE_CHECKING constant is always False at runtime
    # but type-checking tools will evaluate the contents of that block.
    from Scripts.Scene.Scenes.Scene import Scene
    #from Scripts.GameObject.GameObject import GameObject


class SceneManager:
    '''
    切換場景(Scene)

    呼叫當前場景更新
    '''
    current_scene: Scene = None
    to_load_scene: Scene = None

    @staticmethod
    def change_scene(new_scene: Scene):
        SceneManager.to_load_scene = new_scene

    @staticmethod
    def initialization():
        if not SceneManager.current_scene:
            return
        SceneManager.current_scene.on_instantiate()

    @staticmethod
    def physics():
        if not SceneManager.current_scene:
            return
        SceneManager.current_scene.physics_update()

    @staticmethod
    def update():
        if not SceneManager.current_scene:
            return
        SceneManager.current_scene.update()

    @staticmethod
    def rendering():
        if not SceneManager.current_scene:
            return
        SceneManager.current_scene.on_will_render_object()

    @staticmethod
    def decommissioning():
        if SceneManager.current_scene:
            
            if SceneManager.to_load_scene:
                SceneManager.current_scene.on_release()

            SceneManager.current_scene.on_destroy()

        if SceneManager.to_load_scene:
            SceneManager.current_scene = SceneManager.to_load_scene
            SceneManager.to_load_scene = None
            SceneManager.current_scene.on_load()
