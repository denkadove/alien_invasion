import pygame
from pygame.sprite import Group

import game_functions as gf
from settings import Settings
from mage import Mage


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Goblin Invasion')
    mage = Mage(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, mage, aliens)

    while True:
        gf.check_events(ai_settings, screen, mage, bullets)
        mage.update()
        gf.update_bullets(aliens, bullets)
        gf.update_aliens(ai_settings, aliens)
        gf.update_screen(ai_settings, screen, mage, aliens, bullets)


run_game()
