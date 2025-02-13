import pygame
from enum import Enum
from os import path

pygame.font.init()


class GameSetting(Enum):
    width = 1000
    height = 800
    size = width, height
    window = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 50)
    fps = 8


class ShipImage(Enum):
    giant = pygame.transform.flip(
        pygame.transform.scale(
            pygame.image.load(path.join("static", "ship", "giant.png")),
            (int(1000 * 1 / 12), int(800 * 1 / 10)),
        ),
        flip_x=False,
        flip_y=True,
    )
    leader = pygame.transform.scale(
        pygame.image.load(path.join("static", "ship", "leader.png")),
        (int(1000 * 1 / 14), int(800 * 1 / 14)),
    )

    player = pygame.transform.scale(
        pygame.image.load(path.join("static", "ship", "player.png")),
        (100, 80),
    )
    rocket = pygame.transform.scale(
        pygame.image.load(path.join("static", "ship", "rocket.png")),
        (int(1000 * 1 / 22), int(800 * 1 / 22)),
    )
    ufo = pygame.transform.scale(
        pygame.image.load(path.join("static", "ship", "ufo.png")),
        (int(1000 * 1 / 22), int(800 * 1 / 22)),
    )
    genetic = [
        pygame.transform.flip(
            pygame.image.load(path.join("static", "ship", "genetic.png")),
            flip_x=False,
            flip_y=True,
        ),
        pygame.image.load(path.join("static", "ship", "small-green.png")),
        pygame.image.load(path.join("static", "ship", "small-red.png")),
        pygame.transform.flip(
            pygame.transform.scale(
                pygame.image.load(path.join("static", "ship", "small-yellow.png")),
                (40, 33),
            ),
            flip_x=True,
            flip_y=True,
        ),
    ]


class BulletImage(Enum):
    circular_red = pygame.transform.scale(
        pygame.image.load(path.join("static", "bullet", "circulatory-red.png")),
        (30, 25),
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
    heart = pygame.transform.scale(
        pygame.image.load(path.join("static", "utility", "heart.png")),
        (40, 35),
    )


class Color(Enum):
    white = 255, 255, 255
    black = 0, 0, 0
    red = 255, 0, 0
    green = 0, 255, 0
