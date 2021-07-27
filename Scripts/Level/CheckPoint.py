
from Scripts.Locals import CharacterID
from pygame import Rect, Vector3
from Scripts.Physics.Box import Box


class Checkpoint:
    def __init__(self) -> None:
        self.trigger_box: Box = None
        self.physics_activity_box: Box = None
        self.render_activity_rect: Rect = None
        self.enemies: list[tuple[CharacterID, Vector3]] = []
        self.detecting = False

