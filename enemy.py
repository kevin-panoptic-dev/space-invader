import pygame, numpy as np
from constants import ShipImage, Color, BulletImage, GameSetting
from abstract import EnemyShip, Bullet
from pygame.surface import Surface
from typing import Optional


class GeneticEnemy(EnemyShip):
    def __init__(self) -> None:
        super().__init__()
        self.ship_image = ShipImage.genetic.value
        self.weapon_image = [
            BulletImage.hyperbolic_blue.value,
            BulletImage.hyperbolic_green.value,
            BulletImage.hyperbolic_red.value,
            BulletImage.hyperbolic_yellow.value,
        ]
        self.health = 1.0
        self.multiplier = 10
        self.alive = True
        self.velocity = 1.0

    def draw(self, window: Surface) -> None:
        if self.alive:
            window.blit(self.ship_image, (self.x, self.y))

    def move(self) -> None:
        return super().move()

    def health_bar(self, window: Surface) -> None:
        return None

    def collide(self, objects: list[Bullet]) -> None:
        return super().collide(objects)

    def attack(self) -> None:
        raise NotImplementedError("method is not implemented yet.")


class GiantEnemy(EnemyShip):
    def __init__(self) -> None:
        super().__init__()
        self.ship_image = ShipImage.giant.value
        self.health = 5.0
        self.multiplier = 1
        self.current_health = 5.0
        self.weapon_image = [
            BulletImage.hyperbolic_blue.value,
            BulletImage.hyperbolic_green.value,
            BulletImage.hyperbolic_red.value,
            BulletImage.hyperbolic_yellow.value,
        ]
        self.alive = True
        self.velocity = 0.3

    def move(self) -> None:
        return super().move()

    def draw(self, window: Surface) -> None:
        if self.alive:
            window.blit(self.ship_image, (self.x, self.y))

    def health_bar(self, window: Surface):
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
                int(self.ship_image.get_width() * self.current_health / self.health),
                8,
            ),
        )

    def collide(self, objects: list[Bullet]) -> None:
        return super().collide(objects)

    def attack(self) -> None:
        raise NotImplementedError("method is not implemented yet.")


class UfoEnemy(EnemyShip):
    def __init__(self) -> None:
        super().__init__()
        self._direction: Optional[str] = None

        self.ship_image = ShipImage.ufo.value
        self.health = 2.0
        self.multiplier = 2
        self.current_health = 2.0
        self.weapon_image = [BulletImage.circular_red.value]
        self.alive = True
        self.velocity = 1.5

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

    def health_bar(self, window: Surface):
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
                int(self.ship_image.get_width() * self.current_health / self.health),
                6,
            ),
        )

    def collide(self, objects: list[Bullet]) -> None:
        return super().collide(objects)

    def attack(self) -> None:
        raise NotImplementedError("method is not implemented yet.")

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
        self.alive = True

    def draw(self, window: Surface) -> None:
        if self.alive:
            window.blit(self.ship_image, (self.x, self.y))

    def health_bar(self, window: Surface):
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
                int(self.ship_image.get_width() * self.current_health / self.health),
                6,
            ),
        )

    def collide(self, objects: list[Bullet]) -> None:
        return super().collide(objects)

    def attack(self) -> None:
        raise NotImplementedError("method is not implemented yet.")
