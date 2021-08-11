from __future__ import annotations
from Scripts.Locals import SwitchButtonEvent
from Scripts.Tools.Action import Action
from Scripts.Button.Button import Button




class SwitchButton(Button):

    def __init__(self) -> None:
        super().__init__()
        self.pressed = False
        self.switch_event: dict[SwitchButtonEvent, Action] = {
            SwitchButtonEvent.open: Action(),
            SwitchButtonEvent.close: Action()
        }

    def set_default_SwitchButtonEvent(self, pressed=False):
        self.pressed = pressed

    def down(self):
        self.switch_event[SwitchButtonEvent.close if not self.pressed else SwitchButtonEvent.open].notify()
        self.pressed = not self.pressed
        return super().down()

    def get_switch_button_event(self, state: SwitchButtonEvent):
        return self.switch_event[state]
