import random, time
from pygame.surface import Surface
from abstract import ComradeShip
from utility import shoot
from constants import ShipImage, BulletImage
from game import is_available


class RocketComrade(ComradeShip):
    def __init__(self) -> None:
        super().__init__()
        self.ship_image = ShipImage.rocket.value
        self.weapon_image = [
            BulletImage.hyperbolic_blue.value,
            BulletImage.hyperbolic_green.value,
            BulletImage.hyperbolic_red.value,
            BulletImage.hyperbolic_yellow.value,
        ]
        self.health = 1.0
        self.multiplier = 1
        self.velocity = 0.5
        self.cool_down_limit = 1.8

    def attack(self) -> None:
        if not is_available(self.last_shoot_time, self.cool_down_limit):
            return

        shoot(
            self.x + self.ship_image.get_width() / 2,
            self.y + self.ship_image.get_height() * 1.2,
            random.choice(self.weapon_image),
            "enemy",
            "hyperbolic",
        )
        self.last_shot_time = time.time()

    def collide(self, objects: list) -> None:
        return super().collide(objects)

    def health_bar(self, window: Surface) -> None:
        return None

    def move(self) -> None:
        return super().move()

    def draw(self, window: Surface) -> None:
        if self.alive:
            window.blit(self.ship_image, (self.x, self.y))
