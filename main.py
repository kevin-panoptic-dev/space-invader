import pygame, numpy as np, random, time, copy, sys
from pygame.surface import Surface
from core import (
    MAX_ITERATION,
    GLOBAL_COMRADE_BULLET_LIST,
    GLOBAL_ENEMY_BULLET_LIST,
    GLOBAL_ENEMY_SHIP_LIST,
    GLOBAL_COMRADE_SHIP_LIST,
)
from comrade import RocketComrade
from enemy import UfoEnemy, GeneticEnemy, GiantEnemy, LeaderEnemy
from weapon import (
    EnemyHyperbolicBullet,
    ComradeHyperbolicBullet,
    EnemyCircularBullet,
    EnemyEliteBullet,
)
from player import Player
from constants import GameSetting, UtilityImage
from pymodule.utility import silence
from utility import parse, init


window = GameSetting.window.value
ufo_multiplier = UfoEnemy().multiplier
genetic_multiplier = GeneticEnemy().multiplier
giant_multiplier = GiantEnemy().multiplier
leader_multiplier = LeaderEnemy().multiplier
comrade_multiplier = RocketComrade().multiplier


# def draw_mask(
#     surface: pygame.Surface, mask: pygame.mask.MaskType, position: tuple[int, int]
# ) -> None:
#     mask_width, mask_height = mask.get_size()
#     overlay_color = (0, 255, 0, 100)

#     for y_coord in range(mask_height):
#         for x_coord in range(mask_width):
#             if mask.get_at((x_coord, y_coord)):
#                 pygame.draw.rect(
#                     surface=surface,
#                     color=overlay_color,
#                     rect=(position[0] + x_coord, position[1] + y_coord, 1, 1),
#                 )

positive_unbound = lambda x, height: x + height > GameSetting.height.value
negative_unbound = lambda x: x < 0
is_comrade = lambda ship: isinstance(ship, RocketComrade)


def is_overlap(
    positions: list[tuple[float, float]], interim: int, x: int, y: int
) -> bool:
    if not len(positions):
        return False

    for x_coordinate, y_coordinate in positions:
        if x < x_coordinate and x + interim >= x_coordinate:  # x is in the left
            # above check and below check
            if (y < y_coordinate and y + interim >= y_coordinate) or (
                y > y_coordinate and y - interim <= y_coordinate
            ):
                return True
        elif x > x_coordinate and x - interim <= x_coordinate:  # x in in the right
            # above check and below check
            if (y < y_coordinate and y + interim >= y_coordinate) or (
                y > y_coordinate and y - interim <= y_coordinate
            ):
                return True
    return False


def populate(wave: int):
    global GLOBAL_COMRADE_SHIP_LIST, GLOBAL_COMRADE_BULLET_LIST, GLOBAL_ENEMY_BULLET_LIST, GLOBAL_ENEMY_SHIP_LIST
    if not isinstance(wave, int):
        raise TypeError(f"Expected int for wave, got {type(wave).__name__}")

    ufo_number = int(np.floor(ufo_multiplier * wave) / 5)
    genetic_number = int(np.floor(genetic_multiplier * wave) / 5)
    giant_number = int(np.floor(giant_multiplier * wave) / 5)
    leader_number = int(np.floor(leader_multiplier * wave) / 5)
    comrade_number = int(np.floor(comrade_multiplier * wave) / 5)

    GLOBAL_ENEMY_SHIP_LIST.extend((UfoEnemy() for _ in range(ufo_number)))
    GLOBAL_ENEMY_SHIP_LIST.extend((GiantEnemy() for _ in range(giant_number)))
    GLOBAL_ENEMY_SHIP_LIST.extend((GeneticEnemy() for _ in range(genetic_number)))
    GLOBAL_ENEMY_SHIP_LIST.extend((LeaderEnemy() for _ in range(leader_number)))
    GLOBAL_COMRADE_SHIP_LIST.extend((RocketComrade() for _ in range(comrade_number)))

    required_upper_height = int(
        50 * len(GLOBAL_ENEMY_BULLET_LIST) / 5 + 200 * 0.1 * wave
    )
    required_lower_height = int(
        50 * 0.2 * len(GLOBAL_COMRADE_SHIP_LIST) / 5 + 200 * 0.1 * wave
    )
    enemy_positions = []
    comrade_positions = []

    for ship in GLOBAL_COMRADE_SHIP_LIST:
        while True:
            y = int(
                np.random.randint(
                    GameSetting.height.value,
                    required_lower_height + GameSetting.height.value,
                )
            )
            x = int(np.random.randint(0, GameSetting.width.value))
            if is_overlap(comrade_positions, 50, x, y):
                continue
            ship.x = x
            ship.y = y
            comrade_positions.append((x, y))
            break

    for ship in GLOBAL_ENEMY_SHIP_LIST:
        while True:
            y = int(np.random.randint(-required_upper_height, 0))
            x = int(np.random.randint(20, GameSetting.width.value - 120))
            if is_overlap(enemy_positions, 50, x, y):
                continue
            ship.x = x
            ship.y = y
            enemy_positions.append((x, y))
            break

    # for ship in GLOBAL_SHIP_LIST:
    #     if not isinstance(ship, RocketComrade):
    #         while True:
    #             y = int(np.random.randint(-required_upper_height, 0))
    #             x = int(np.random.randint(20, GameSetting.width.value - 120))
    #             if is_overlap(enemy_positions, 50, x, y):
    #                 continue
    #             ship.x = x
    #             ship.y = y
    #             enemy_positions.append((x, y))
    #             break
    #     else:
    #         while True:
    #             y = int(
    #                 np.random.randint(
    #                     GameSetting.height.value,
    #                     required_lower_height + GameSetting.height.value,
    #                 )
    #             )
    #             x = int(np.random.randint(0, GameSetting.width.value))
    #             if is_overlap(comrade_positions, 50, x, y):
    #                 continue
    #             ship.x = x
    #             ship.y = y
    #             enemy_positions.append((x, y))
    #             break
    # else:
    #     del (
    #         enemy_positions,
    #         comrade_positions,
    #         required_lower_height,
    #         required_upper_height,
    #     )


def draw(life: int, player: Player):
    global GLOBAL_COMRADE_SHIP_LIST, GLOBAL_COMRADE_BULLET_LIST, GLOBAL_ENEMY_BULLET_LIST, GLOBAL_ENEMY_SHIP_LIST
    heart = UtilityImage.heart.value
    window.blit(UtilityImage.background.value, (0, 0))

    for ship in GLOBAL_COMRADE_SHIP_LIST:
        ship.draw(window)
        ship.move()
        GLOBAL_COMRADE_BULLET_LIST = ship.attack(GLOBAL_COMRADE_BULLET_LIST)
        ship.collide(GLOBAL_ENEMY_BULLET_LIST)
        # ship.health_bar(window)
        # if is_comrade(ship):
        if negative_unbound(ship.y):
            ship.alive = False
            life += 1
        # else:
        #     if positive_unbound(ship.y, ship.ship_image.get_height()):
        #         ship.alive = False
        #         life -= 1
        #     else:
        #         offset_x = player.x - ship.x
        #         offset_y = player.y - ship.y
        #         is_overlap = player.mask.overlap(ship.mask, (offset_x, offset_y))
        #         if is_overlap:
        #             ship.alive = False
        #             player.current_health -= np.random.randint(10, 50)

    for ship in GLOBAL_ENEMY_SHIP_LIST:
        ship.draw(window)
        ship.move()
        GLOBAL_ENEMY_BULLET_LIST = ship.collide(GLOBAL_ENEMY_BULLET_LIST)
        if positive_unbound(ship.y, ship.ship_image.get_height()):
            ship.alive = False
            life -= 1
        else:
            offset_x = player.x - ship.x
            offset_y = player.y - ship.y
            is_overlap = player.mask.overlap(ship.mask, (offset_x, offset_y))
            if is_overlap:
                ship.alive = False
                player.current_health -= np.random.randint(10, 50)

    for bullet in GLOBAL_ENEMY_BULLET_LIST:
        bullet.draw(window)
        bullet.move()
        bullet.collide([*GLOBAL_COMRADE_SHIP_LIST, player])
        if positive_unbound(bullet.y, bullet.image.get_height()):
            bullet.alive = False

    for bullet in GLOBAL_COMRADE_BULLET_LIST:
        bullet.draw(window)
        bullet.move()
        bullet.collide(GLOBAL_ENEMY_SHIP_LIST)
        if negative_unbound(bullet.y):
            bullet.alive = False

    # for bullet in GLOBAL_BULLET_LIST:
    #     assert (
    #         isinstance(bullet, EnemyEliteBullet)
    #         or isinstance(bullet, EnemyCircularBullet)
    #         or isinstance(bullet, EnemyHyperbolicBullet)
    #         or isinstance(bullet, ComradeHyperbolicBullet)
    #     )
    #     bullet.draw(window)
    #     bullet.move()
    #     bullet.collide([*GLOBAL_SHIP_LIST, player])
    #     if isinstance(bullet, ComradeHyperbolicBullet):
    #         if negative_unbound(bullet.y):
    #             bullet.alive = False
    #     else:
    #         if positive_unbound(bullet.y, bullet.image.get_height()):
    #             bullet.alive = False

    for x in range(life):
        window.blit(heart, (10 + x * (10 + heart.get_width()), 10))

    player.draw(window)
    player.collide(GLOBAL_ENEMY_BULLET_LIST)
    # draw_mask(window, player.mask, (int(player.x), int(player.y)))
    pygame.display.update()


def main(user: str):
    global GLOBAL_COMRADE_BULLET_LIST, GLOBAL_ENEMY_SHIP_LIST, GLOBAL_COMRADE_SHIP_LIST, GLOBAL_ENEMY_BULLET_LIST
    life = 5
    player = Player(user=user)
    clock = GameSetting.clock.value

    for wave in range(MAX_ITERATION):
        populate(wave + 1)
        while True:
            clock.tick(60)
            draw(life, player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            move_x = 0
            move_y = 0

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                GLOBAL_COMRADE_BULLET_LIST = player.attack(GLOBAL_COMRADE_BULLET_LIST)

            move_x = 0  # Initialize move_x
            move_y = 0  # Initialize move_y

            if (
                keys[pygame.K_a]
                and not keys[pygame.K_d]
                and player.x - player.velocity > 0
            ):
                move_x = -1  # Move left (negative x)
            elif (
                keys[pygame.K_d]
                and not keys[pygame.K_a]
                and player.x + player.velocity + player.ship_image.get_width()
                < GameSetting.width.value
            ):
                move_x = 1  # Move right (positive x)

            if (
                keys[pygame.K_w]
                and not keys[pygame.K_s]
                and player.y - player.velocity > 0
            ):
                move_y = -1  # Move up (negative y)
            elif (
                keys[pygame.K_s]
                and not keys[pygame.K_w]
                and player.y + player.velocity + player.ship_image.get_height() * 1.2
                < GameSetting.height.value
            ):
                move_y = 1  # Move down (positive y)

            player.move(move_x, move_y)

            # for ship in GLOBAL_SHIP_LIST:
            #     assert (
            #         isinstance(ship, UfoEnemy)
            #         or isinstance(ship, RocketComrade)
            #         or isinstance(ship, GiantEnemy)
            #         or isinstance(ship, LeaderEnemy)
            #         or isinstance(ship, GeneticEnemy)
            #     )
            #     ship.move()
            #     GLOBAL_BULLET_LIST = ship.attack(GLOBAL_BULLET_LIST)
            #     ship.collide(GLOBAL_BULLET_LIST)
            #     ship.health_bar(window)
            #     if is_comrade(ship):
            #         if negative_unbound(ship.y):
            #             ship.alive = False
            #             life += 1
            #     else:
            #         if positive_unbound(ship.y, ship.ship_image.get_height()):
            #             ship.alive = False
            #             life -= 1
            #         else:
            #             offset_x = player.x - ship.x
            #             offset_y = player.y - ship.y
            #             is_overlap = player.mask.overlap(
            #                 ship.mask, (offset_x, offset_y)
            #             )
            #             if is_overlap:
            #                 ship.alive = False
            #                 player.current_health -= np.random.randint(10, 50)

            # for bullet in GLOBAL_BULLET_LIST:
            #     assert (
            #         isinstance(bullet, EnemyEliteBullet)
            #         or isinstance(bullet, EnemyCircularBullet)
            #         or isinstance(bullet, EnemyHyperbolicBullet)
            #         or isinstance(bullet, ComradeHyperbolicBullet)
            #     )
            #     bullet.draw(window)
            #     bullet.collide(GLOBAL_SHIP_LIST)
            #     if isinstance(bullet, ComradeHyperbolicBullet):
            #         if negative_unbound(bullet.y):
            #             bullet.alive = False
            #     else:
            #         if positive_unbound(bullet.y, bullet.image.get_height()):
            #             bullet.alive = False

            GLOBAL_COMRADE_BULLET_LIST = list(
                filter(lambda bullet: bullet.alive, GLOBAL_COMRADE_BULLET_LIST)
            )
            GLOBAL_ENEMY_BULLET_LIST = list(
                filter(lambda bullet: bullet.alive, GLOBAL_ENEMY_BULLET_LIST)
            )
            GLOBAL_ENEMY_SHIP_LIST = list(
                filter(lambda ship: ship.alive, GLOBAL_ENEMY_SHIP_LIST)
            )
            GLOBAL_COMRADE_SHIP_LIST = list(
                filter(lambda ship: ship.alive, GLOBAL_COMRADE_SHIP_LIST)
            )

            if not len(GLOBAL_ENEMY_SHIP_LIST):
                player.hiatus()
                break

            # println = lambda *x: np.random.random() > 0.95 and print(*x)

            # println(len(GLOBAL_BULLET_LIST))
            pygame.display.update()

            if life <= 0 or player.current_health <= 0 or not player.alive:
                print("exit")
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    init()
    user = parse()
    main(user)
