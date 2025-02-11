import pygame, numpy as np, random, time, copy, sys
from core import MAX_ITERATION, GLOBAL_SHIP_LIST, GLOBAL_BULLET_LIST
from comrade import ComradeShip
from enemy import UfoEnemy, GeneticEnemy, GiantEnemy, LeaderEnemy
from player import Player
from constants import GameSetting
from pymodule.utility import silence


user = "some_user"
player = Player(user="")


@silence()
def main():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    move_x = 0
    move_y = 0

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        player.attack()

    if keys[pygame.K_a] and not keys[pygame.K_d] and player.y - player.velocity > 0:
        move_y = -1
    elif (
        keys[pygame.K_d]
        and not keys[pygame.K_a]
        and player.y + player.velocity + player.ship_image.get_width()
        < GameSetting.width.value
    ):
        move_y = 1

    if keys[pygame.K_w] and not keys[pygame.K_s] and player.x - player.velocity > 0:
        move_x = -1
    elif (
        keys[pygame.K_s]
        and not keys[pygame.K_w]
        and player.x + player.velocity + player.ship_image.get_height() * 1.2
        < GameSetting.height.value
    ):
        move_y = 1

    player.move(move_x, move_y)


if __name__ == "__main__":
    main()
