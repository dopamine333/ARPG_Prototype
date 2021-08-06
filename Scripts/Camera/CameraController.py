from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Camera.Camera import Camera
from pygame import Rect, Vector2, Vector3
from Scripts.GameObject.GameObject import GameObject
from Scripts.GameObject.Component import Component


class CameraController(Component):
    '''
    跟隨一個遊戲物件(GameObject)

    可設定跟隨軸向和設定活動範圍

    屬性:
        offset: Vector = (0,0,0)
        follow_speed: float = 0.8 in range [0, 1]
        follow_axis: tuple[bool,bool,bool] = (True, True, True)
    '''

    def __init__(self) -> None:
        super().__init__()
        self.target: Vector3 = None
        self.offset = Vector3()
        self.follow_axis = (True, True, True)
        self.follow_speed = 0.3
        self.max_follow_distance=10
        self.camera: Camera = None
        self.activity_rect: Rect = None
    

    def start(self):
        self.camera = self.get_component(Camera)
        if self.target:
            self.position.xyz = self.target+self.offset
    # region setter
    def set_activity_rect(self, activity_rect: Rect):
        self.activity_rect = activity_rect
    def set_target(self, target: Vector3):
        self.target = target
        if not self.follow_axis[0]:
            self.position.x=self.target.x+self.offset.x
        if not self.follow_axis[1]:
            self.position.y=self.target.y+self.offset.y
        if not self.follow_axis[2]:
            self.position.z=self.target.z+self.offset.z

    def set_offset(self, offset: Vector3):
        self.offset = Vector3(offset)

    def set_follow_speed(self, follow_speed: float):
        self.follow_speed = follow_speed

    def set_max_follow_distance(self, max_follow_distance: float):
        self.max_follow_distance = max_follow_distance

    def set_follow_axis(self, x=True, y=True, z=True):
        self.follow_axis = (x, y, z)
    # endregion        

    def update(self):
        if self.target:
            to=self.target+self.offset-self.position
            if not self.follow_axis[0]:
                to.x=0
            if not self.follow_axis[1]:
                to.y=0
            if not self.follow_axis[2]:
                to.z=0
            distance=to.length()
            if distance<0.01:
                return
            #計算要移動的向量
            distance = min(distance*self.follow_speed,self.max_follow_distance)
            to.scale_to_length(distance)

            if self.follow_axis[0]:
                dx,dy=to.x*self.camera.world_to_screen_matrix[0]
                if dx>0:
                    if self.camera.view_rect.right+dx<self.activity_rect.right:
                        if dy>0:
                            if self.camera.view_rect.bottom+dy<self.activity_rect.bottom:
                                self.position.x+=to.x
                        elif dy<0:
                            if self.camera.view_rect.top+dy>self.activity_rect.top:
                                self.position.x+=to.x
                        else:
                            self.position.x+=to.x
                elif dx<0:
                    if self.camera.view_rect.left+dx>self.activity_rect.left:
                        if dy>0:
                            if self.camera.view_rect.bottom+dy<self.activity_rect.bottom:
                                self.position.x+=to.x
                        elif dy<0:
                            if self.camera.view_rect.top+dy>self.activity_rect.top:
                                self.position.x+=to.x
                        else:
                            self.position.x+=to.x
                else:
                    if dy>0:
                        if self.camera.view_rect.bottom+dy<self.activity_rect.bottom:
                            self.position.x+=to.x
                    elif dy<0:
                        if self.camera.view_rect.top+dy>self.activity_rect.top:
                            self.position.x+=to.x
                    else:
                        self.position.x+=to.x
            if self.follow_axis[1]:
                dx,dy=to.y*self.camera.world_to_screen_matrix[1]
                if dx>0:
                    if self.camera.view_rect.right+dx<self.activity_rect.right:
                        if dy>0:
                            if self.camera.view_rect.bottom+dy<self.activity_rect.bottom:
                                self.position.y+=to.y
                        elif dy<0:
                            if self.camera.view_rect.top+dy>self.activity_rect.top:
                                self.position.y+=to.y
                        else:
                            self.position.y+=to.y
                elif dx<0:
                    if self.camera.view_rect.left+dx>self.activity_rect.left:
                        if dy>0:
                            if self.camera.view_rect.bottom+dy<self.activity_rect.bottom:
                                self.position.y+=to.y
                        elif dy<0:
                            if self.camera.view_rect.top+dy>self.activity_rect.top:
                                self.position.y+=to.y
                        else:
                            self.position.y+=to.y
                else:
                    if dy>0:
                        if self.camera.view_rect.bottom+dy<self.activity_rect.bottom:
                            self.position.y+=to.y
                    elif dy<0:
                        if self.camera.view_rect.top+dy>self.activity_rect.top:
                            self.position.y+=to.y
                    else:
                        self.position.y+=to.y
            if self.follow_axis[2]:
                dx,dy=to.z*self.camera.world_to_screen_matrix[2]
                if dx>0:
                    if self.camera.view_rect.right+dx<self.activity_rect.right:
                        if dy>0:
                            if self.camera.view_rect.bottom+dy<self.activity_rect.bottom:
                                self.position.z+=to.z
                        elif dy<0:
                            if self.camera.view_rect.top+dy>self.activity_rect.top:
                                self.position.z+=to.z
                        else:
                            self.position.z+=to.z
                elif dx<0:
                    if self.camera.view_rect.left+dx>self.activity_rect.left:
                        if dy>0:
                            if self.camera.view_rect.bottom+dy<self.activity_rect.bottom:
                                self.position.z+=to.z
                        elif dy<0:
                            if self.camera.view_rect.top+dy>self.activity_rect.top:
                                self.position.z+=to.z
                        else:
                            self.position.z+=to.z
                else:
                    if dy>0:
                        if self.camera.view_rect.bottom+dy<self.activity_rect.bottom:
                            self.position.z+=to.z
                    elif dy<0:
                        if self.camera.view_rect.top+dy>self.activity_rect.top:
                            self.position.z+=to.z
                    else:
                        self.position.z+=to.z

                
                

                        