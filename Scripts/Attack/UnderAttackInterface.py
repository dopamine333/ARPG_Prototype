from Scripts.GameObject.Component import Component
from Scripts.Attack.AttackParam import AttackParam


class UnderAttackInterface(Component):
    '''能被攻擊的組件都要繼承此'''

    def under_attack(self, attack_param: AttackParam):
        pass
