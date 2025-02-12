import pygame, numpy as np
from abc import abstractmethod, ABC
from pygame.surface import Surface
from typing import Optional
from constants import BulletImage, GameSetting
from game import is_intersecting


class Bullet(ABC):
    def __init__(self) -> None:
        self._power: Optional[float]
        self._x: Optional[float]
        self._y: Optional[float]
        self._image: Optional[Surface]
        self._group: Optional[str]
        self._alive: Optional[bool]
        self._x_velocity: Optional[float]
        self._y_velocity: Optional[float]

    @abstractmethod
    def move(self):
        pass

    def collide(self, objects: list):
        objects = list(
            filter(lambda ship: ship.group != self.group and ship.alive, objects)
        )
        collided_objects = is_intersecting(self, objects)

        if len(collided_objects):
            self.alive = False
            print("kill a bullet")

    @property
    def y_velocity(self):
        if not isinstance(self._y_velocity, (float, int)):
            raise RuntimeError(f"self.y_velocity is not defined yet.")
        return self._y_velocity

    @y_velocity.setter
    def y_velocity(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._y_velocity = value

    @y_velocity.deleter
    def y_velocity(self):
        self._y_velocity = None

    @property
    def x_velocity(self):
        if not isinstance(self._x_velocity, (float, int)):
            raise RuntimeError(f"self.x_velocity is not defined yet.")
        return self._x_velocity

    @x_velocity.setter
    def x_velocity(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._x_velocity = value

    @x_velocity.deleter
    def x_velocity(self):
        self._x_velocity = None

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
    def mask(self):
        mask = pygame.mask.from_surface(self.image)
        return mask

    @property
    def image(self):
        if not isinstance(self._image, Surface):
            raise RuntimeError(f"self.image is not defined yet.")
        return self._image

    @image.setter
    def image(self, value: Surface):
        if not isinstance(value, Surface):
            raise TypeError(f"Expected Surface, got {type(value).__name__}.")
        self._image = value

    @image.deleter
    def image(self):
        self._image = None

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

    @property
    def power(self):
        if not isinstance(self._power, (float, int)):
            raise RuntimeError(f"self.power is not defined yet.")
        return self._power

    @power.setter
    def power(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Expected float, got {type(value).__name__}.")
        self._power = value

    @power.deleter
    def power(self):
        self._power = None


class EnemyBullet(Bullet):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self.group = "enemy"
        self.alive = True

    def draw(self, window: Surface):
        if self.alive:
            window.blit(self.image, (self.x, self.y))


class ComradeBullet(Bullet):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self.group = "comrade"
        self.alive = True

    def draw(self, window: Surface):
        if self.alive:
            window.blit(self.image, (self.x, self.y))


class ComradeHyperbolicBullet(ComradeBullet):
    def __init__(self) -> None:
        super().__init__()
        self.power = 15
        self.x_velocity = 0
        self.y_velocity = 4

    def move(self):
        self.y -= self.y_velocity
        if self.y + self.image.get_height() < 0:
            self.alive = False


class EnemyHyperbolicBullet(EnemyBullet):
    def __init__(self) -> None:
        super().__init__()
        self.power = 10
        self.x_velocity = 0
        self.y_velocity = 4

    def move(self):
        self.y += self.y_velocity
        if self.y > GameSetting.height.value:
            self.alive = False


class EnemyCircularBullet(EnemyBullet):
    def __init__(self) -> None:
        super().__init__()
        self.image = BulletImage.circular_red.value
        self.power = 7.5
        self.x_velocity = 2 if np.random.random() > 0.5 else -2
        self.y_velocity = 2

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        if self.y > GameSetting.height.value:
            self.alive = False
            return

        if self.x + self.image.get_width() > GameSetting.width.value or self.x < 0:
            self.x_velocity = -self.x_velocity


class EnemyEliteBullet(EnemyBullet):
    def __init__(self) -> None:
        super().__init__()
        self.image = BulletImage.elite.value
        self.power = 1
        self.x_velocity = 0
        self.y_velocity = 1.2

    def move(self):
        self.y += self.y_velocity
        if self.y > GameSetting.height.value:
            self.alive = False

    def collide(self, objects):
        pass
