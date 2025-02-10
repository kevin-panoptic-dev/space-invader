from abc import ABC, abstractmethod
from typing import Optional
from pygame.surface import Surface


class Ship(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self._x: Optional[float]
        self._y: Optional[float]
        self._health: Optional[float]
        self._ship_image: Optional[Surface]
        self._weapon_image: Optional[list[Surface]]
        self._alive: Optional[bool]
        self._cool_down_limit: Optional[float]

    @abstractmethod
    def draw(self, window: Surface) -> None:
        pass

    @abstractmethod
    def attack(self) -> None:
        pass

    @abstractmethod
    def health_bar(self) -> None:
        pass

    @abstractmethod
    def collide(self) -> None:
        pass

    @property
    def cool_down_limit(self):
        if not isinstance(self._cool_down_limit, float):
            raise RuntimeError(f"self.cool_down_limit is not defined yet.")
        return self._cool_down_limit

    @cool_down_limit.setter
    def cool_down_limit(self, value):
        if not isinstance(value, float):
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
    def alive(self, value):
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
    def weapon_image(self, value):
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
    def ship_image(self, value):
        if not isinstance(value, Surface):
            raise TypeError(f"Expected Surface, got {type(value).__name__}.")
        self._ship_image = value

    @ship_image.deleter
    def ship_image(self):
        self._ship_image = None

    @property
    def health(self):
        if not isinstance(self._health, float):
            raise RuntimeError(f"self.health is not defined yet.")
        return self._health

    @health.setter
    def health(self, value):
        if not isinstance(value, float):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._health = value

    @health.deleter
    def health(self):
        self._health = None

    @property
    def y(self):
        if not isinstance(self._y, float):
            raise RuntimeError(f"self.y is not defined yet.")
        return self._y

    @y.setter
    def y(self, value):
        if not isinstance(value, float):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._y = value

    @y.deleter
    def y(self):
        self._y = None

    @property
    def x(self):
        if not isinstance(self._x, float):
            raise RuntimeError(f"self.x is not defined yet.")
        return self._x

    @x.setter
    def x(self, value):
        if not isinstance(value, float):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._x = value

    @x.deleter
    def x(self):
        self._x = None
