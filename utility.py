import pygame
from pymodule.debug import vibrenthe
from pymodule.utility import silence
from pygame.surface import Surface
from typing import Literal
from core import GLOBAL_BULLET_LIST
from weapon import (
    EnemyEliteBullet,
    EnemyCircularBullet,
    EnemyHyperbolicBullet,
    ComradeHyperbolicBullet,
)

groupType = Literal["comrade", "enemy"]
weaponType = Literal["elite", "circular", "hyperbolic"]


@silence()
def init():
    pygame.font.init()
    pygame.display.set_caption("Space Invader")


def collect_data():
    try:
        vibrenthe(
            "Enter preferred health, between 50 and 500: >>>",
            usefile=False,
            useline=False,
            color=vibrenthe.GREEN,
            end="",
        )

        health = round(float(input()), 2)
        if not 50 <= health <= 500:
            raise ValueError("Health must between 50 and 500")

        vibrenthe(
            "Enter preferred velocity, between 1.0 and 5.0: >>>",
            usefile=False,
            useline=False,
            color=vibrenthe.GREEN,
            end="",
        )
        velocity = round(float(input()), 2)

        if not 1.0 <= velocity <= 5.0:
            raise ValueError("Velocity must between 1.0 and 5.0")

        vibrenthe(
            "Enter preferred cool down interval, between 0.3 and 2.0: >>>",
            usefile=False,
            useline=False,
            color=vibrenthe.GREEN,
            end="",
        )
        cool_down_limit = round(float(input()), 2)

        if not 0.3 <= cool_down_limit <= 2.0:
            raise ValueError("Cool down must between 0.3 and 2.0")

        vibrenthe(
            "Enter preferred restored_health, between 0 and 50: >>>",
            usefile=False,
            useline=False,
            color=vibrenthe.GREEN,
            end="",
        )
        restored_health = round(float(input()), 2)

        if not 0 <= restored_health <= 50:
            raise ValueError("Restored health must between 0 and 50")

        return {
            "health": health,
            "velocity": velocity,
            "cool_down_limit": cool_down_limit,
            "restored_health": restored_health,
        }

    except Exception as error:
        vibrenthe(f"INVALID INPUT: {error}!")
        return collect_data()


def shoot(x: float, y: float, image: Surface, group: groupType, weapon: weaponType):
    match group:
        case "comrade":
            if weapon == "hyperbolic":
                bullet = ComradeHyperbolicBullet()
                bullet.image = image
            else:
                raise ValueError(
                    f"Unrecognized group weapon type {weapon} for comrade."
                )
        case "enemy":
            match weapon:
                case "circular":
                    bullet = EnemyCircularBullet()
                case "elite":
                    bullet = EnemyEliteBullet()
                case "hyperbolic":
                    bullet = EnemyHyperbolicBullet()
                    bullet.image = image
                case _:
                    raise ValueError(f"Unrecognized weapon {weapon}.")
        case _:
            raise ValueError(f"Unrecognized group {group}.")

    bullet.x = x
    bullet.y = y
    GLOBAL_BULLET_LIST.append(bullet)
