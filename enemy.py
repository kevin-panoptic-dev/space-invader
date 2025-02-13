import pygame, numpy as np, random, time
from constants import ShipImage, Color, BulletImage, GameSetting
from abstract import EnemyShip
from pygame.surface import Surface
from typing import Optional
from utility import shoot
from game import is_available


class GeneticEnemy(EnemyShip):
    def __init__(self) -> None:
        super().__init__()
        self.ship_image = random.choice(ShipImage.genetic.value)
        self.weapon_image = [
            BulletImage.hyperbolic_blue.value,
            BulletImage.hyperbolic_green.value,
            BulletImage.hyperbolic_red.value,
            BulletImage.hyperbolic_yellow.value,
        ]
        self.health = 1.0
        self.multiplier = 10
        self.velocity = 1.0
        self.cool_down_limit = 4
        self.current_health = 1.0

    def draw(self, window: Surface) -> None:
        if self.alive:
            window.blit(self.ship_image, (self.x, self.y))

    def move(self) -> None:
        return super().move()

    def health_bar(self, window: Surface) -> None:
        return None

    def collide(self, objects: list) -> None:
        return super().collide(objects)

    def attack(self, bullet_list: list):
        if not is_available(self.last_shoot_time, self.cool_down_limit):
            return bullet_list

        bullet_list = shoot(
            self.x + self.ship_image.get_width() / 2,
            self.y + self.ship_image.get_height() * 1.2,
            random.choice(self.weapon_image),
            "enemy",
            "hyperbolic",
            bullet_list,
        )
        self.last_shoot_time = time.time()
        return bullet_list


class GiantEnemy(EnemyShip):
    def __init__(self) -> None:
        super().__init__()
        self.ship_image = ShipImage.giant.value
        self.health = 2.5
        self.multiplier = 1
        self.current_health = 2.5
        self.weapon_image = [
            BulletImage.hyperbolic_blue.value,
            BulletImage.hyperbolic_green.value,
            BulletImage.hyperbolic_red.value,
            BulletImage.hyperbolic_yellow.value,
        ]
        self.velocity = 0.8
        self.cool_down_limit = 6

    def move(self) -> None:
        return super().move()

    def draw(self, window: Surface) -> None:
        if self.alive:
            window.blit(self.ship_image, (self.x, self.y))
            pygame.draw.rect(
                window,
                Color.red.value,
                (
                    self.x,
                    self.y + self.ship_image.get_height() + 10,
                    self.ship_image.get_width(),
                    8,
                ),
            )
            pygame.draw.rect(
                window,
                Color.green.value,
                (
                    self.x,
                    self.y + self.ship_image.get_height() + 10,
                    int(
                        self.ship_image.get_width() * self.current_health / self.health
                    ),
                    8,
                ),
            )

    def health_bar(self, window: Surface):
        pass

    def collide(self, objects: list) -> None:
        return super().collide(objects)

    def attack(self, bullet_list: list):
        if not is_available(self.last_shoot_time, self.cool_down_limit):
            return bullet_list

        bullet_list = shoot(
            self.x + self.ship_image.get_width() / 2,
            self.y + self.ship_image.get_height() * 1.2,
            random.choice(self.weapon_image),
            "enemy",
            "hyperbolic",
            bullet_list,
        )
        self.last_shoot_time = time.time()
        return bullet_list


class UfoEnemy(EnemyShip):
    def __init__(self) -> None:
        super().__init__()
        self._direction: Optional[str] = None
        self.ship_image = ShipImage.ufo.value
        self.health = 2.0
        self.multiplier = 5
        self.current_health = 2.0
        self.weapon_image = [BulletImage.circular_red.value]
        self.velocity = 1.5
        self.cool_down_limit = 2.0

    def move(self):
        if self.direction == None:
            if self.x < GameSetting.width.value / 2:
                self.direction = "right"
            else:
                self.direction = "left"
        else:
            if self.direction == "left":
                if self.x - self.ship_image.get_width() < 0:
                    self.direction = "right"
            else:
                if self.x + self.ship_image.get_width() * 2 > GameSetting.width.value:
                    self.direction = "left"

        x_motion = np.sqrt(3) / 2 * self.velocity
        y_motion = self.velocity / 2
        if self.direction == "right":
            self.x += x_motion
        else:
            self.x -= x_motion
        self.y += y_motion

    def draw(self, window: Surface) -> None:
        if self.alive:
            window.blit(self.ship_image, (self.x, self.y))
            pygame.draw.rect(
                window,
                Color.red.value,
                (
                    self.x,
                    self.y + self.ship_image.get_height() + 10,
                    self.ship_image.get_width(),
                    6,
                ),
            )
            pygame.draw.rect(
                window,
                Color.green.value,
                (
                    self.x,
                    self.y + self.ship_image.get_height() + 10,
                    int(
                        self.ship_image.get_width() * self.current_health / self.health
                    ),
                    6,
                ),
            )

    def health_bar(self, window: Surface):
        pass

    def collide(self, objects: list) -> None:
        return super().collide(objects)

    def attack(self, bullet_list: list):
        if not is_available(self.last_shoot_time, self.cool_down_limit):
            return bullet_list
        bullet_list = shoot(
            self.x,
            self.y + self.ship_image.get_height() * 1,
            random.choice(self.weapon_image),
            "enemy",
            "circular",
            bullet_list,
        )
        shoot(
            self.x + self.ship_image.get_width(),
            self.y + self.ship_image.get_height() * 1,
            random.choice(self.weapon_image),
            "enemy",
            "circular",
            bullet_list,
        )
        self.last_shoot_time = time.time()
        return bullet_list

    @property
    def direction(self):
        # if not isinstance(self._direction, str):
        #     raise RuntimeError(f"self.direction is not defined yet.")
        return self._direction

    @direction.setter
    def direction(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value).__name__}.")
        self._direction = value

    @direction.deleter
    def direction(self):
        self._direction = None


class LeaderEnemy(EnemyShip):
    def __init__(self) -> None:
        super().__init__()
        self.ship_image = ShipImage.ufo.value
        self.health = 10.0
        self.multiplier = 0.3
        self.current_health = 10.0
        self.weapon_image = [BulletImage.elite.value]
        self.cool_down_limit = 20
        self.velocity = 0.3

    def draw(self, window: Surface) -> None:
        if self.alive:
            window.blit(self.ship_image, (self.x, self.y))
            pygame.draw.rect(
                window,
                Color.red.value,
                (
                    self.x,
                    self.y + self.ship_image.get_height() + 10,
                    self.ship_image.get_width(),
                    6,
                ),
            )
            pygame.draw.rect(
                window,
                Color.green.value,
                (
                    self.x,
                    self.y + self.ship_image.get_height() + 10,
                    int(
                        self.ship_image.get_width() * self.current_health / self.health
                    ),
                    6,
                ),
            )

    def move(self):
        return super().move()

    def health_bar(self, window: Surface):
        pass

    def collide(self, objects: list) -> None:
        return super().collide(objects)

    def attack(self, bullet_list: list):
        if not is_available(self.last_shoot_time, self.cool_down_limit):
            return bullet_list
        bullet_list = shoot(
            self.x,
            self.y + self.ship_image.get_height() * 1.2,
            random.choice(self.weapon_image),
            "enemy",
            "elite",
            bullet_list,
        )
        self.last_shoot_time = time.time()
        return bullet_list
