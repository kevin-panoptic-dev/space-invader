import pygame, numpy as np
from abc import ABC, abstractmethod
from typing import Optional
from pygame.surface import Surface
from game import is_intersecting


class Ship(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self._x: Optional[float]
        self._y: Optional[float]
        self._health: Optional[float]
        self._current_health: Optional[float]
        self._ship_image: Optional[Surface]
        self._weapon_image: Optional[list[Surface]]
        self._alive: Optional[bool]
        self._cool_down_limit: Optional[float]
        self._multiplier: Optional[float]
        self._velocity: Optional[float]
        self._group: Optional[str]
        self._last_shoot_time: Optional[float]

    @abstractmethod
    def draw(self, window: Surface) -> None:
        pass

    @abstractmethod
    def attack(self, bullet_list: list):
        return bullet_list

    @abstractmethod
    def health_bar(self, window: Surface) -> None:
        pass

    @abstractmethod
    def collide(self, objects: list) -> None:
        # objects = list(
        #     filter(lambda bullet: bullet.group != self.group and bullet.alive, objects)
        # )
        collided_objects = is_intersecting(self, objects)
        if not len(collided_objects):
            return

        total_damage = np.sum([bullet.power for bullet in collided_objects])
        self.current_health -= total_damage
        if self.current_health < 0:
            self.alive = False

    @abstractmethod
    def move(self) -> None:
        pass

    @property
    def last_shoot_time(self):
        if not isinstance(self._last_shoot_time, (float, int)):
            raise RuntimeError(f"self.last_shoot_time is not defined yet.")
        return self._last_shoot_time

    @last_shoot_time.setter
    def last_shoot_time(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._last_shoot_time = value

    @last_shoot_time.deleter
    def last_shoot_time(self):
        self._last_shoot_time = None

    @property
    def velocity(self):
        if not isinstance(self._velocity, (float, int)):
            raise RuntimeError(f"self.velocity is not defined yet.")
        return self._velocity

    @velocity.setter
    def velocity(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._velocity = value

    @velocity.deleter
    def velocity(self):
        self._velocity = None

    @property
    def current_health(self):
        if not isinstance(self._current_health, (float, int)):
            raise RuntimeError(f"self.current_health is not defined yet.")
        return self._current_health

    @current_health.setter
    def current_health(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._current_health = value

    @current_health.deleter
    def current_health(self):
        self._current_health = None

    @property
    def group(self):
        if not isinstance(self._group, str):
            raise RuntimeError(f"self.group is not defined yet.")
        return self._group

    @group.setter
    def group(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value).__name__}.")
        self._group = value

    @group.deleter
    def group(self):
        self._group = None

    @property
    def multiplier(self):
        if not isinstance(self._multiplier, (float, int)):
            raise RuntimeError(f"self.multiplier is not defined yet.")
        return self._multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._multiplier = value

    @multiplier.deleter
    def multiplier(self):
        self._multiplier = None

    @property
    def mask(self) -> pygame.Mask:
        mask = pygame.mask.from_surface(self.ship_image)
        return mask

    @property
    def cool_down_limit(self):
        if not isinstance(self._cool_down_limit, (float, int)):
            raise RuntimeError(f"self.cool_down_limit is not defined yet.")
        return self._cool_down_limit

    @cool_down_limit.setter
    def cool_down_limit(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._cool_down_limit = value

    @cool_down_limit.deleter
    def cool_down_limit(self):
        self._cool_down_limit = None

    @property
    def alive(self):
        if not isinstance(self._alive, bool):
            raise RuntimeError(f"self.alive is not defined yet.")
        return self._alive

    @alive.setter
    def alive(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got {type(value).__name__}.")
        self._alive = value

    @alive.deleter
    def alive(self):
        self._alive = None

    @property
    def weapon_image(self):
        if not isinstance(self._weapon_image, list):
            raise RuntimeError(f"self.weapon_image is not defined yet.")
        return self._weapon_image

    @weapon_image.setter
    def weapon_image(self, value: list[Surface]):
        if not isinstance(value, list):
            raise TypeError(f"Expected list, got {type(value).__name__}.")
        self._weapon_image = value

    @weapon_image.deleter
    def weapon_image(self):
        self._weapon_image = None

    @property
    def ship_image(self):
        if not isinstance(self._ship_image, Surface):
            raise RuntimeError(f"self.ship_image is not defined yet.")
        return self._ship_image

    @ship_image.setter
    def ship_image(self, value: Surface):
        if not isinstance(value, Surface):
            raise TypeError(f"Expected Surface, got {type(value).__name__}.")
        self._ship_image = value

    @ship_image.deleter
    def ship_image(self):
        self._ship_image = None

    @property
    def health(self):
        if not isinstance(self._health, (float, int)):
            raise RuntimeError(f"self.health is not defined yet.")
        return self._health

    @health.setter
    def health(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._health = value

    @health.deleter
    def health(self):
        self._health = None

    @property
    def y(self):
        if not isinstance(self._y, (float, int)):
            raise RuntimeError(f"self.y is not defined yet.")
        return self._y

    @y.setter
    def y(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._y = value

    @y.deleter
    def y(self):
        self._y = None

    @property
    def x(self):
        if not isinstance(self._x, (float, int)):
            raise RuntimeError(f"self.x is not defined yet.")
        return self._x

    @x.setter
    def x(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._x = value

    @x.deleter
    def x(self):
        self._x = None


class EnemyShip(Ship):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self.group = "enemy"
        self.alive = True
        self.last_shoot_time = 0

    @abstractmethod
    def draw(self, window: Surface) -> None:
        return super().draw(window)

    @abstractmethod
    def attack(self, bullet_list: list):
        return super().attack(bullet_list)

    @abstractmethod
    def health_bar(self, window: Surface) -> None:
        return super().health_bar(window)

    @abstractmethod
    def move(self) -> None:
        self.y += self.velocity

    @abstractmethod
    def collide(self, objects: list) -> None:
        return super().collide(objects)


class ComradeShip(Ship):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self.group = "comrade"
        self.alive = True
        self.last_shoot_time = 0

    @abstractmethod
    def draw(self, window: Surface) -> None:
        return super().draw(window)

    @abstractmethod
    def attack(self, bullet_list: list):
        return super().attack(bullet_list)

    @abstractmethod
    def health_bar(self, window: Surface) -> None:
        return super().health_bar(window)

    @abstractmethod
    def collide(self, objects: list) -> None:
        return super().collide(objects)

    @abstractmethod
    def move(self) -> None:
        self.y -= self.velocity
