import pygame
from pygame.locals import *
import random

from sprites import Sprite


class BaseFood(Sprite):

    def __init__(self, position, speed=[0, 0], image=None):
        self.acceleration = [3, 3]

        Sprite.__init__(self, image, position, speed)

    # def do_collision(self):
    #     if self.get_lives() == 0:
    #         self.kill()
    #     else:
    #         pass

    # def is_dead(self):
    #     return self.get_lives() == 0

    def accel_left(self):
        speed = self.get_speed()
        self.set_speed(speed[0] - self.acceleration[0], speed[1])

    def accel_right(self):
        speed = self.get_speed()
        self.set_speed(speed[0] + self.acceleration[0], speed[1])

    def is_lost(self):
        return self.get_pos()[1] >= 600


class Food(BaseFood):

    foods = [
        {'image': './imagens/doce.png', 'points': 1},
        {'image': './imagens/tomate.png', 'points': 1},
        {'image': './imagens/apple_juice.png', 'points': 1},
        {'image': './imagens/avocado_maki.png', 'points': 1},
        {'image': './imagens/bacon.png', 'points': 1},
        {'image': './imagens/banana_donut.png', 'points': 1},
        {'image': './imagens/banana.png', 'points': 1},
        {'image': './imagens/blackberry_juice.png', 'points': 1},
        {'image': './imagens/broccoli.png', 'points': 1},
        {'image': './imagens/cabbage.png', 'points': 1},
        {'image': './imagens/california_temaki.png', 'points': 1},
        {'image': './imagens/candy_cane.png', 'points': 1},
        {'image': './imagens/candy_stick.png', 'points': 1},
        {'image': './imagens/burger.png', 'points': 1},
        {'image': './imagens/cheese_cake.png', 'points': 1},
        {'image': './imagens/cheese_croissant.png', 'points': 1},
        {'image': './imagens/cherries.png', 'points': 1},
        {'image': './imagens/chicken_leg.png', 'points': 1},
        {'image': './imagens/chili_pepper.png', 'points': 1},
        {'image': './imagens/chocolate_balls.png', 'points': 1},
        {'image': './imagens/chocolate_bar.png', 'points': 1},
        {'image': './imagens/chocolate_cake.png', 'points': 1},
        {'image': './imagens/chocolate_cereal.png', 'points': 1},
        {'image': './imagens/chocolate_croissant.png', 'points': 1},
        {'image': './imagens/chocolate_cupcake.png', 'points': 1},
    ]

    def __init__(self, position, speed=None):
        food = random.choice(self.foods)

        image = food['image']
        points = food['points']
        BaseFood.__init__(self, position, speed, image)