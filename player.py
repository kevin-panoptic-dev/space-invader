import pygame, pickle, random, numpy as np
from pygame.surface import Surface
from typing import Optional
from constants import ShipImage, BulletImage, GameSetting
from abstract import Bullet, ComradeShip
from utility import collect_data, shoot
from typing import override, Literal

move_type = Literal[0, 1, -1]


class Player(ComradeShip):
    def __init__(self, user: str) -> None:
        if not isinstance(user, str):
            raise TypeError(f"Expected str for user, got {type(user).__name__}")

        super().__init__()
        self._restored_health = 0.0

        try:
            with open("data.pickle", "rb") as file:
                all_data: dict[str, dict[str, float]] = pickle.load(file)
                if user in all_data.keys():
                    dataset = all_data.get(user)
                    if dataset is not None:
                        self.health = dataset["health"]
                        self.current_health = self.health
                        self.velocity = dataset["velocity"]
                        self.cool_down_limit = dataset["cool_down_limit"]
                        self.restored_health = dataset["restored_health"]
                    else:
                        new_dataset = collect_data()
                        self.health = new_dataset["health"]
                        self.current_health = self.health
                        self.velocity = new_dataset["velocity"]
                        self.cool_down_limit = new_dataset["cool_down_limit"]
                        self.restored_health = new_dataset["restored_health"]
                        all_data[user] = new_dataset
                        with open("data.pickle", "rb") as file:
                            pickle.dump({user: all_data}, file)

        except FileNotFoundError:
            dataset = collect_data()
            self.health = dataset["health"]
            self.current_health = self.health
            self.velocity = dataset["velocity"]
            self.cool_down_limit = dataset["cool_down_limit"]
            self.restored_health = dataset["restored_health"]
            with open("data.pickle", "rb") as file:
                pickle.dump({user: dataset}, file)

        self.ship_image = ShipImage.player.value
        self.weapon_image = [
            BulletImage.hyperbolic_blue.value,
            BulletImage.hyperbolic_green.value,
            BulletImage.hyperbolic_red.value,
            BulletImage.hyperbolic_yellow.value,
        ]
        self.x = GameSetting.width.value / 2 - self.ship_image.get_width() / 2
        self.y = GameSetting.height.value * 0.9 - self.ship_image.get_height() / 3

    def collide(self, objects: list[Bullet]) -> None:
        super().collide(objects)

    def attack(self) -> None:
        shoot(
            self.x + self.ship_image.get_width() / 4,
            self.y - self.ship_image.get_height() * 1,
            random.choice(self.weapon_image),
            "comrade",
            "hyperbolic",
        )
        shoot(
            self.x + self.ship_image.get_width() * 3 / 4,
            self.y - self.ship_image.get_height() * 1,
            random.choice(self.weapon_image),
            "comrade",
            "circular",
        )

    @override
    def move(self, x: move_type, y: move_type) -> None:  # type: ignore (override)
        if x != 0 and y != 0:
            speed = np.sqrt(self.velocity)
        else:
            speed = self.velocity

        match x:
            case 0:
                match 0:
                    case 0:
                        pass
                    case 1:
                        self.y += speed
                    case -1:
                        self.y -= speed
                    case _:
                        raise ValueError(f"Unrecognized y move type {y}.")
            case 1:
                match 0:
                    case 0:
                        self.x += speed
                    case 1:
                        self.x += speed
                        self.y += speed
                    case -1:
                        self.y -= speed
                        self.x += speed
                    case _:
                        raise ValueError(f"Unrecognized y move type {y}.")
            case -1:
                match 0:
                    case 0:
                        self.x -= speed
                    case 1:
                        self.x -= speed
                        self.y += speed
                    case -1:
                        self.y -= speed
                        self.x -= speed
                    case _:
                        raise ValueError(f"Unrecognized y move type {y}.")
            case _:
                raise ValueError(f"Unrecognized x move type {x}.")

    def draw(self, window: Surface) -> None:
        window.blit(self.ship_image, (self.x, self.y))

    def hiatus(self):
        if self.current_health + self.restored_health > self.health:
            self.current_health = self.health
            return
        self.current_health += self.restored_health

    @property
    def restored_health(self):
        if not isinstance(self._restored_health, float):
            raise RuntimeError(f"self.restored_health is not defined yet.")
        return self._restored_health

    @restored_health.setter
    def restored_health(self, value: float):
        if not isinstance(value, float):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._restored_health = value

    @restored_health.deleter
    def restore_health(self):
        self._restored_health = None
