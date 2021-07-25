from Scripts.Locals import Face
from Scripts.Character.CharacterBrain.EnemyBrain import EnemyBrain


class SlimeBrain(EnemyBrain):
    def __init__(self) -> None:
        super().__init__()
        self.blocking_range_squared = 250**2

    def set_blocking_range(self, blocking_range: float):
        self.blocking_range_squared = blocking_range**2

    def update(self):
        if self.target:
            vector = self.target.position-self.character.position
            self.character.move(vector.xz)
            if self.target.position.distance_squared_to(self.character.position) < self.blocking_range_squared:
                if self.target.rigidbody.get_surface(Face.down) > self.character.rigidbody.get_surface(Face.up):
                    self.character.jump()
