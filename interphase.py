import pygame
import sys
from constants import GameSetting, UtilityImage, Color
from pygame.surface import Surface
from utility import init

init()


def menu(window: Surface, clock: pygame.time.Clock):
    clock.tick(GameSetting.fps.value)
    in_menu = True

    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                in_menu = False
                break

        window.blit(UtilityImage.background.value, (0, 0))
        title_label = GameSetting.font.value.render(
            "Press any key to begin...", 1, Color.white.value
        )
        window.blit(
            title_label,
            (
                GameSetting.width.value // 2 - title_label.get_width() // 2,
                GameSetting.height.value // 2,
            ),
        )
        pygame.display.update()
