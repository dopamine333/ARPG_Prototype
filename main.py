from Scripts.Scene.SceneManager import SceneManager
import pygame
from Scripts.Scene.Scenes.StartScene import StartScene
from Scripts.GameLoop.GameLoop import GameLoop
if __name__ == "__main__":
    gameLoop = GameLoop()
    SceneManager.change(StartScene())
    gameLoop.run()
