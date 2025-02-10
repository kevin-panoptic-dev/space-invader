import pygame
from enum import Enum
from os import path

pygame.font.init()
pygame.display.set_caption("Space Invader")


class GameSetting(Enum):
    width = 1000
    height = 800
    size = width, height
    window = pygame.display.set_mode(size)
    Clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 50)


class ShipImage(Enum):
    genetic = pygame.image.load(path.join("static", "ship", "genetic.png"))
    giant = pygame.image.load(path.join("static", "ship", "giant.png"))
    leader = pygame.image.load(path.join("static", "ship", "leader.png"))
    player = pygame.image.load(path.join("static", "ship", "player.png"))
    rocket = pygame.image.load(path.join("static", "ship", "rocket.png"))
    ufo = pygame.image.load(path.join("static", "ship", "ufo.png"))


class BulletImage(Enum):
    circular_red = pygame.image.load(
        path.join("static", "bullet", "circulatory-red.png")
    )
    elite = pygame.image.load(path.join("static", "bullet", "elite.png"))
    hyperbolic_blue = pygame.image.load(
        path.join("static", "bullet", "hyperbolic-blue.png")
    )
    hyperbolic_green = pygame.image.load(
        path.join("static", "bullet", "hyperbolic-green.png")
    )
    hyperbolic_red = pygame.image.load(
        path.join("static", "bullet", "hyperbolic-red.png")
    )
    hyperbolic_yellow = pygame.image.load(
        path.join("static", "bullet", "hyperbolic-yellow.png")
    )


class UtilityImage(Enum):
    background = pygame.transform.scale(
        pygame.image.load(path.join("static", "utility", "background.png")),
        size=GameSetting.size.value,
    )
    heart = pygame.image.load(path.join("static", "utility", "heart.png"))


class Color(Enum):
    white = 255, 255, 255
    black = 0, 0, 0
    red = 255, 0, 0
    green = 0, 255, 0
