from Scripts.CharacterBrain.EnemyBrain import EnemyBrain

class SlimeBrain(EnemyBrain):
    def update(self):
        if self.target:
            vector = self.target.get_position()-self.character.get_position()
            self.character.move(vector.xz)