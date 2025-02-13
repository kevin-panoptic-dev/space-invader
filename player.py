import pickle, random, numpy as np, time, pygame
from pygame.surface import Surface
from typing import Optional
from constants import ShipImage, BulletImage, GameSetting, Color
from abstract import ComradeShip
from utility import collect_data, shoot
from typing import override, Literal
from game import is_available, is_intersecting

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
                        with open("data.pickle", "wb") as file:
                            pickle.dump({user: all_data}, file)

        except FileNotFoundError:
            dataset = collect_data()
            self.health = dataset["health"]
            self.current_health = self.health
            self.velocity = dataset["velocity"]
            self.cool_down_limit = dataset["cool_down_limit"]
            self.restored_health = dataset["restored_health"]
            with open("data.pickle", "wb") as file:
                pickle.dump({user: dataset}, file)

        self.ship_image = ShipImage.player.value
        self.weapon_image = [
            BulletImage.hyperbolic_blue.value,
            BulletImage.hyperbolic_green.value,
            BulletImage.hyperbolic_red.value,
            BulletImage.hyperbolic_yellow.value,
        ]
        self.x = GameSetting.width.value / 2 - self.ship_image.get_width() / 2
        self.y = GameSetting.height.value * 0.9 - self.ship_image.get_height()
        self.cool_down_limit /= 3
        self.velocity *= 1.5

    def collide(self, objects: list) -> bool:  # type: ignore (override)
        collided_objects = is_intersecting(self, objects)
        if not len(collided_objects):
            return False

        total_damage = np.sum([bullet.power for bullet in collided_objects])
        self.current_health -= total_damage
        if self.current_health < 0:
            self.current_health = self.health * 2 / 3
            return True
        return False

    def attack(self, bullet_list: list):
        if not is_available(self.last_shoot_time, self.cool_down_limit):
            return bullet_list

        bullet_list = shoot(
            self.x + self.ship_image.get_width() / 4,
            self.y - self.ship_image.get_height() / 2,
            random.choice(self.weapon_image),
            "comrade",
            "hyperbolic",
            bullet_list,
        )
        bullet_list = shoot(
            self.x - self.ship_image.get_width() / 4,
            self.y - self.ship_image.get_height() / 2,
            random.choice(self.weapon_image),
            "comrade",
            "hyperbolic",
            bullet_list,
        )
        self.last_shoot_time = time.time()
        return bullet_list

    def health_bar(self, window: Surface) -> None:
        pass

    @override
    def move(self, x: move_type, y: move_type) -> None:  # type: ignore (override)
        if x == 0 and y == 0:
            return  # No movement

        # Calculate magnitude of movement vector
        magnitude = np.sqrt(x**2 + y**2)

        # Normalize the movement vector (important for diagonal movement)
        if magnitude > 0:  # Avoid division by zero
            x /= magnitude
            y /= magnitude

        # Apply velocity
        self.x += x * self.velocity
        self.y += y * self.velocity

    def draw(self, window: Surface) -> None:
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
                int(self.ship_image.get_width() * self.current_health / self.health),
                6,
            ),
        )

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
