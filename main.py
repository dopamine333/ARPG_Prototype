from Scripts.Scene.Scenes.StartScene import StartScene
from Scripts.GameLoop.GameLoop import GameLoop
if __name__=="__main__":
    gameLoop=GameLoop()
    gameLoop.scene_changer.change(StartScene(gameLoop.scene_changer))
    gameLoop.run()

