from Scripts.Time.Invoker import Invoker
from Scripts.GameObject.Component import Component


class LifeTimer(Component):
    '''
    生命倒計時器

    設定一個時間，到了後自動銷毀物件

    屬性:
        +lifetime: float
    '''

    def __init__(self) -> None:
        super().__init__()
        self.lifetime = 0

    def start(self):
        Invoker.invoke(self.destroy, self.lifetime)

    def on_destroy(self):
        if Invoker.is_invoking(self.destroy):
            Invoker.cancel_invoke(self.destroy)

    def set_lifetime(self, lifetime: float):
        self.lifetime = lifetime
