from Scripts.Character.CharacterBrain.EnemyBrain import EnemyBrain


class SlimeBrain(EnemyBrain):
    def update(self):
        if self.target:
            vector = self.target.position-self.character.position
            self.character.move(vector.xz)
