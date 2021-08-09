from Scripts.Factory.OnLevelGameObjectFactory import OnLevelGameObjectFactory
from Scripts.Factory.CharacterFactory import CharacterFactory
from Scripts.Tools.Singleton import Singleton


class FactoryManager(Singleton):
    def __init__(self) -> None:
        self.characterfactory = CharacterFactory()
        self.onlevelgameobjectfactory = OnLevelGameObjectFactory()

    def get_characterfactory(self):
        return self.characterfactory

    def get_onlevelgameobjectfactory(self):
        return self.onlevelgameobjectfactory
