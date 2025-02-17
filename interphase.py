import pygame
import sys
from constants import GameSetting, UtilityImage, Color
from pygame.surface import Surface
from utility import init

init()


def menu(window: Surface, clock: pygame.time.Clock):
    in_menu = True
    title_label = GameSetting.font.value.render(
        "Press any key to begin...", 1, Color.white.value
    )

    while in_menu:
        clock.tick(GameSetting.fps.value)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                in_menu = False
                break

        window.blit(UtilityImage.background.value, (0, 0))
        window.blit(
            title_label,
            (
                GameSetting.width.value // 2 - title_label.get_width() // 2,
                GameSetting.height.value // 2,
            ),
        )
        pygame.display.update()


def finish(window: Surface, clock: pygame.time.Clock):
    game_over_label = GameSetting.font.value.render("You Lose!", 1, Color.white.value)
    replay_label = GameSetting.font.value.render(
        "Press any key to replay...", 1, Color.white.value
    )
    wait_time = 240

    while True:
        clock.tick(GameSetting.fps.value)
        wait_time -= 1
        if wait_time <= 0:
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return True

        window.blit(UtilityImage.background.value, (0, 0))
        window.blit(
            game_over_label,
            (
                GameSetting.width.value // 2 - game_over_label.get_width() // 2,
                GameSetting.height.value // 2 - game_over_label.get_height() // 2,
            ),
        )
        window.blit(
            replay_label,
            (
                GameSetting.width.value // 2 - replay_label.get_width() // 2,
                GameSetting.height.value // 2 + replay_label.get_height(),
            ),
        )
        pygame.display.update()


def next(window: Surface, clock: pygame.time.Clock):
    continue_label = GameSetting.font.value.render(
        "Press any key to continue...", 1, Color.white.value
    )
    next_label = GameSetting.font.value.render("Next Wave!", 1, Color.white.value)
    interim_time = 240

    while True:
        clock.tick(GameSetting.fps.value)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return

        interim_time -= 1
        if interim_time <= 0:
            interim_time = 240
            return

        window.blit(
            UtilityImage.background.value,
            (0, 0),
        )
        window.blit(
            continue_label,
            (
                GameSetting.width.value // 2 - continue_label.get_width() // 2,
                GameSetting.height.value // 2 + continue_label.get_height(),
            ),
        )
        window.blit(
            next_label,
            (
                GameSetting.width.value // 2 - next_label.get_width() // 2,
                GameSetting.height.value // 2 - next_label.get_height() // 2,
            ),
        )
        pygame.display.update()
