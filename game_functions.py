import sys
import pygame

from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, mage, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, mage, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, mage)


def check_keyup_event(event, mage):
    if event.key == pygame.K_d:
        mage.moving_right = False
    elif event.key == pygame.K_a:
        mage.moving_left = False
    elif event.key == pygame.K_w:
        mage.moving_up = False
    elif event.key == pygame.K_s:
        mage.moving_down = False


def check_keydown_event(event, ai_settings, screen, mage, bullets):
    if event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_d:
        mage.moving_right = True
    elif event.key == pygame.K_a:
        mage.moving_left = True
    elif event.key == pygame.K_w:
        mage.moving_up = True
    elif event.key == pygame.K_s:
        mage.moving_down = True
    elif event.key == pygame.K_RETURN:
        fire_bullet(ai_settings, screen, mage, bullets)


def update_screen(ai_settings, screen, mage, aliens, bullets):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    mage.blitme()
    aliens.draw(screen)
    pygame.display.flip()


def update_bullets(aliens, bullets):
    """Обновляет позиции пуль и удаляет старые пули."""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        # Проверка попаданий в пришельцев.
        # При обнаружении попадания удалить пулю и пришельца.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)


def fire_bullet(ai_settings, screen, mage, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, mage)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, mage, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, mage.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)


def get_number_rows(ai_settings, mage_height, alien_height):
    """Определяет количество рядов, помещающихся на экране."""
    available_space_y = (ai_settings.screen_height - (10 * alien_height) - mage_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens):
    """
    Проверяет, достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

