from Scripts.Physics.RigidBody import RigidBody
class FrozenRigidBody(RigidBody):
    def update(self):
        self.velocity*=0