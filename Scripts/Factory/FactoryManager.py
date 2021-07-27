from Scripts.Factory.CharacterFactory import CharacterFactory
from Scripts.Tools.Singleton import Singleton
class FactoryManager(Singleton):
    def __init__(self) -> None:
        self.characterfactory=CharacterFactory()
    def get_characterfactory(self):
        return self.characterfactory