from pygame.draw import ellipse
from Scripts.Locals import Layer
from Scripts.Graph.Image import Image
import pygame
from pygame import Surface, Vector2, Vector3

# TODO 完成畫sprite和camera移動


class Camera:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        '''
        self.position=Vector3()
        self.shadow_color = (20, 20, 30, 20)
        self.sprite_orders: list[DrawSpriteOrder] = []
        self.world_to_screen_matrix: list[Vector2] = [
            Vector2(1, 0),  # x
            Vector2(0, -1),  # y
            Vector2(0, -0.2),  # z
        ]
        '''

        transparent_surface = Surface(
            screen.get_size(), pygame.SRCALPHA).convert_alpha()
        self.layers: dict[Layer, Surface] = {
            Layer.UI: transparent_surface.copy(),
            # Layer.sprite: transparent_surface.copy(),
            # Layer.shadow: transparent_surface.copy(),
            # Layer.environment: transparent_surface.copy(),
        }

    def update(self):
        pass

    def draw(self):
        # clear screen
        self.screen.fill((150, 150, 150))
        '''
        #region draw sprites and shadow
        # 將sprite_orders根據z軸由遠排到近(大排到小)
        self.sprite_orders.sort(
            key=lambda order: order.position.z, reverse=True)
        for order in self.sprite_orders:
            # 在Layer.sprite層上畫出sprite
            source = order.image.source
            position = self.world_to_screen(order.position)
            topleft = order.image.offset(position)
            self.layers[Layer.sprite].blit(source, topleft)

            # 在Layer.shadow層上畫出橢圓形的shadow
            shadow_rect = Rect(
                0, 0,
                order.shadow_size.x*self.world_to_screen_matrix[0],
                order.shadow_size.y*self.world_to_screen_matrix[2]
            )
            shadow_rect.center = position
            ellipse(self.layers[Layer.shadow], self.shadow_color, shadow_rect)
        #endregion
        '''
        # region all layers together
        self.screen.blit(self.layers[Layer.UI], (0, 0))
        # endregion

        # region clear all layers
        self.layers[Layer.UI].fill((0, 0, 0, 0))
        # endregion

    def draw_UI(self, image: Image, position: Vector2):
        self.layers[Layer.UI].blit(image.source, image.offset(position))
    '''
    def draw_Sprite(self, image: Image, position: Vector3, shadow_size: Vector2):
        # TODO 把sprite_orders改成二元樹
        self.sprite_orders.append((image, position, shadow_size))

    def world_to_screen(self, world_position: Vector3):
        """
        transform world position to screen position
        """
        screen_position = Vector2()
        screen_position += self.world_to_screen_matrix[0]*world_position.x
        screen_position += self.world_to_screen_matrix[1]*world_position.y
        screen_position += self.world_to_screen_matrix[2]*world_position.z
        screen_position.y += self.screen.get_height()
        return screen_position
    '''


'''
class DrawSpriteOrder:
    def __init__(self, image: Image, position: Vector3, shadow_size: Vector2) -> None:
        self.image = image
        self.position = position
        self.shadow_size = shadow_size
'''
