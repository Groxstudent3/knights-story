import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Меню игры")
font = pygame.font.Font(None, 40)

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

background = pygame.transform.scale(pygame.image.load("фони.jpg"), (WIDTH, HEIGHT))
fantasy_background = pygame.transform.scale(pygame.image.load("замко.jpg"), (WIDTH, HEIGHT))
castle_background = pygame.transform.scale(pygame.image.load("темнота.jpg"), (WIDTH, HEIGHT))
perss_background = pygame.transform.scale(pygame.image.load("войн.png"), (WIDTH, HEIGHT))
boss_background = pygame.transform.scale(pygame.image.load("дракон.png"), (WIDTH, HEIGHT))
player_knight = pygame.transform.scale(pygame.image.load("рицарь-photoroom.png"), (40, 40))
enemy_image = pygame.transform.scale(pygame.image.load("монстер-photoroom.png"), (40, 40))
goal_image = pygame.transform.scale(pygame.image.load("сейв-photoroom.png"), (40, 40))
boss_image = pygame.transform.scale(pygame.image.load("дракон.png"), (150, 150))
player_image = pygame.transform.scale(pygame.image.load("войн.png"), (50, 50))
fireball_image = pygame.transform.scale(pygame.image.load("шару-photoroom.png"), (20, 20))
player_bullet_image = pygame.transform.scale(pygame.image.load("пулля-photoroom.png"), (10, 20))
shoot_sound = pygame.mixer.Sound("metallicheskiy-lyazg-zatvora-pushki.wav")
hit_sound = pygame.mixer.Sound("vyistrel-iz-pushki-27974.wav")
boss_death_sound = pygame.mixer.Sound("ryichanie-drakona.wav")
pygame.mixer.music.load("stranger-things-124008.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
difficulty_settings = {"Легкий": (2, 40), "Средний": (3, 30), "Сложный": (5, 20)}
difficulty = "Средний"

TILE = 40
wall_texture = pygame.image.load("стена.jpg").convert_alpha()
wall_texture = pygame.transform.scale(wall_texture, (TILE, TILE))

def show_message(text, color):
    message = font.render(text, True, color)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)


def draw_button(text, x, y, w, h, pressed=False):
    rect = pygame.Rect(x, y, w, h)
    shadow_rect = rect.copy()
    shadow_rect.move_ip(4, 4)
    shadow_color = (50, 50, 50)
    main_color = (100, 200, 250) if not pressed else (70, 160, 220)
    pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=12)
    pygame.draw.rect(screen, main_color, rect, border_radius=12)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=12)
    text_surf = font.render(text, True, BLACK)
    screen.blit(text_surf, text_surf.get_rect(center=rect.center))
    return rect


def pause_menu():
    while True:
        screen.fill(GRAY)
        title = font.render("Пауза", True, BLACK)
        screen.blit(title, (WIDTH//2 - 50, 50))
        resume_btn = draw_button("Продолжить", 300, 200, 200, 60)
        main_btn = draw_button("Главное меню", 300, 280, 200, 60)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_btn.collidepoint(event.pos):
                    return True
                elif main_btn.collidepoint(event.pos):
                    return False


def game_loop():
    player = pygame.Rect(50, HEIGHT // 2, 40, 40)
    goal = pygame.Rect(WIDTH - 90, HEIGHT // 2, 40, 40)
    enemy = pygame.Rect(300, 100, 40, 40)
    enemy_speed, time_limit = difficulty_settings[difficulty]
    speed = 5
    score = 0
    start_ticks = pygame.time.get_ticks()

    while True:
        screen.blit(background, (0, 0))
        screen.blit(player_knight, player.topleft)
        screen.blit(fireball_image, goal.topleft)
        pygame.draw.rect(screen, YELLOW, enemy)
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(0, time_limit - seconds)
        screen.blit(font.render(f"Время: {remaining_time}", True, BLACK), (10, 10))
        screen.blit(font.render(f"Очки: {score}", True, BLACK), (10, 50))
        if remaining_time == 0:
            show_message("Время вышло!", RED)
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player.x -= speed
        if keys[pygame.K_RIGHT]: player.x += speed
        if keys[pygame.K_UP]: player.y -= speed
        if keys[pygame.K_DOWN]: player.y += speed
        enemy.y += enemy_speed
        if enemy.top <= 0 or enemy.bottom >= HEIGHT:
            enemy_speed = -enemy_speed
        if player.colliderect(goal):
            score += 1
            player.topleft = (50, HEIGHT // 2)
            start_ticks = pygame.time.get_ticks()
        if player.colliderect(enemy):
            show_message("Ты проиграл!", RED)
            return
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if not pause_menu():
                    return


def shooter_game():
    player = pygame.Rect(WIDTH // 2, HEIGHT - 60, 50, 50)
    bullets = []
    boss = pygame.Rect(WIDTH // 2 - 75, 50, 150, 150)
    boss_health = 100
    bullet_speed = 7
    player_speed = 5
    boss_speed = 3
    boss_direction = 1

    boss_bullets = []
    boss_shoot_delay = 1000  # мс
    last_boss_shot = pygame.time.get_ticks()

    while True:
        screen.blit(castle_background, (0, 0))
        keys = pygame.key.get_pressed()

        # Управление игроком
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed
        if keys[pygame.K_SPACE]:
            if len(bullets) == 0 or bullets[-1].y < player.y - 40:
                bullets.append(pygame.Rect(player.centerx - 5, player.top, 10, 20))
                shoot_sound.play()

        # Движение босса
        boss.x += boss_direction * boss_speed
        if boss.left <= 0 or boss.right >= WIDTH:
            boss_direction *= -1

        # Выстрел босса
        current_time = pygame.time.get_ticks()
        if current_time - last_boss_shot > boss_shoot_delay:
            boss_bullets.append(pygame.Rect(boss.centerx - 5, boss.bottom, 10, 20))
            last_boss_shot = current_time

        # Обработка пуль игрока
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.colliderect(boss):
                boss_health -= 5
                bullets.remove(bullet)
                hit_sound.play()
            elif bullet.bottom < 0:
                bullets.remove(bullet)

        # Обработка пуль босса
        for bbullet in boss_bullets[:]:
            bbullet.y += bullet_speed
            if bbullet.colliderect(player):
                show_message("Ты проиграл! Босс попал в тебя!", RED)
                return
            elif bbullet.top > HEIGHT:
                boss_bullets.remove(bbullet)

        # Рисование
        screen.blit(player_image, player.topleft)
        screen.blit(boss_image, boss.topleft)

        for bullet in bullets:
            screen.blit(player_bullet_image, bullet.topleft)
        for bbullet in boss_bullets:
            screen.blit(fireball_image, bbullet.topleft)

        pygame.draw.rect(screen, RED, (10, 10, 200, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, 2 * boss_health, 20))
        screen.blit(font.render(f"Здоровье босса: {boss_health}", True, WHITE), (220, 8))

        if boss_health <= 0:
            boss_death_sound.play()
            show_message("Босс побежден!", GREEN)
            return

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


    while True:
        screen.blit(castle_background, (0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed
        if keys[pygame.K_SPACE]:
            if len(bullets) == 0 or bullets[-1].y < player.y - 40:
                bullets.append(pygame.Rect(player.centerx - 5, player.top, 10, 20))
                shoot_sound.play()

        boss.x += boss_direction * boss_speed
        if boss.left <= 0 or boss.right >= WIDTH:
            boss_direction *= -1

        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.colliderect(boss):
                boss_health -= 10
                bullets.remove(bullet)
                hit_sound.play()
            elif bullet.bottom < 0:
                bullets.remove(bullet)

        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.rect(screen, RED, boss)
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet)

        pygame.draw.rect(screen, RED, (10, 10, 200, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, 2 * boss_health, 20))
        screen.blit(font.render(f"Здоровье босса: {boss_health}", True, WHITE), (220, 8))

        if boss_health <= 0:
            boss_death_sound.play()
            show_message("Босс побежден!", GREEN)
            return

        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()




def settings_menu():
    volume = pygame.mixer.music.get_volume()
    while True:
        screen.fill(GRAY)
        screen.blit(font.render("Настройки", True, BLACK), (330, 40))
        louder_btn = draw_button("Громче", 300, 120, 200, 60)
        quieter_btn = draw_button("Тише", 300, 200, 200, 60)
        back_btn = draw_button("Назад", 300, 280, 200, 60)
        screen.blit(font.render(f"Громкость: {int(volume * 100)}%", True, BLACK), (320, 90))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if louder_btn.collidepoint(event.pos):
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif quieter_btn.collidepoint(event.pos):
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif back_btn.collidepoint(event.pos):
                    return


def difficulty_menu():
    global difficulty
    while True:
        screen.fill(GRAY)
        screen.blit(font.render("Сложность", True, BLACK), (330, 40))
        easy_btn = draw_button("Легкий", 300, 120, 200, 60)
        medium_btn = draw_button("Средний", 300, 200, 200, 60)
        hard_btn = draw_button("Сложный", 300, 280, 200, 60)
        back_btn = draw_button("Назад", 300, 360, 200, 60)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.collidepoint(event.pos):
                    difficulty = "Легкий"
                elif medium_btn.collidepoint(event.pos):
                    difficulty = "Средний"
                elif hard_btn.collidepoint(event.pos):
                    difficulty = "Сложный"
                elif back_btn.collidepoint(event.pos):
                    return


def main_menu():
    while True:
        screen.blit(background, (0, 0))
        screen.blit(font.render("Главное меню", True, BLACK), (300, 50))
        play_btn = draw_button("Играть", 300, 140, 200, 60)
        settings_btn = draw_button("Настройки", 300, 220, 200, 60)
        diff_btn = draw_button("Сложность", 300, 300, 200, 60)
        quit_btn = draw_button("Выход", 300, 380, 200, 60)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    level_menu()
                elif settings_btn.collidepoint(event.pos):
                    settings_menu()
                elif diff_btn.collidepoint(event.pos):
                    difficulty_menu()
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def maze_game(level=1):
    player = pygame.Rect(40, 40, TILE, TILE)
    goal = pygame.Rect(680, 520, TILE, TILE)

    level_maps = {
        1: [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,1,1,1,0,1,0,1,1,1,1,1,1,0,1],
            [1,1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1],
            [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,0,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,0,1,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
            [1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1],
            [1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ],
        2: [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1],
            [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,0,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
            [1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1],
            [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1],
            [1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
    }

    level_map = level_maps.get(level, level_maps[1])

    walls = []
    for y, row in enumerate(level_map):
        for x, tile in enumerate(row):
            if tile == 1:
                walls.append(pygame.Rect(x * TILE, y * TILE, TILE, TILE))

    enemy = pygame.Rect(400, 280, TILE, TILE)
    enemy_path = [(400, 280), (600, 280)]
    enemy_direction = 1
    enemy_speed = 2

    speed = 4

    # таймер для складності
    difficulty_times = {"Легкий": 60, "Средний": 40, "Сложный": 30}
    time_limit = difficulty_times.get(difficulty, 40)
    start_ticks = pygame.time.get_ticks()

    running = True
    while running:
        screen.blit(fantasy_background, (0, 0))
        for wall in walls:
            screen.blit(wall_texture, wall.topleft)
        screen.blit(goal_image, goal.topleft)
        screen.blit(player_knight, player.topleft)
        screen.blit(enemy_image, enemy.topleft)


        # таймер
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(0, time_limit - seconds)
        time_text = font.render(f"Время: {remaining_time}", True, BLACK)
        screen.blit(time_text, (10, 10))
        if remaining_time == 0:
            show_message("Время вышло!", RED)
            return

        pygame.display.flip()
        clock.tick(60)

        target_x, _ = enemy_path[enemy_direction]
        if enemy.x < target_x:
            enemy.x += enemy_speed
        elif enemy.x > target_x:
            enemy.x -= enemy_speed
        if abs(enemy.x - target_x) < enemy_speed:
            enemy_direction = 1 - enemy_direction

        keys = pygame.key.get_pressed()
        new_player = player.copy()
        if keys[pygame.K_LEFT]: new_player.x -= speed
        if keys[pygame.K_RIGHT]: new_player.x += speed
        if keys[pygame.K_UP]: new_player.y -= speed
        if keys[pygame.K_DOWN]: new_player.y += speed
        if not any(new_player.colliderect(w) for w in walls):
            player = new_player

        if player.colliderect(goal):
            show_message("Ты прошёл лабиринт!", GREEN)
            return
        if player.colliderect(enemy):
            show_message("Пойман врагом!", RED)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


# Обновим level_menu, чтобы вызвать maze_game(level=2) для второго уровня

def level_menu():
    while True:
        screen.blit(background, (0, 0))
        draw_button("Выбор уровня", 280, 30, 240, 60)
        levels = [(i + 1, draw_button(f"Уровень {i+1}", 300, 120 + i * 70, 200, 60)) for i in range(3)]
        back_btn = draw_button("Назад", 300, 340, 200, 60)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for level, rect in levels:
                    if rect.collidepoint(event.pos):
                        if level == 1:
                            maze_game(level=1)
                        elif level == 2:
                            maze_game(level=2)
                        elif level == 3:
                            shooter_game()
                        return
                if back_btn.collidepoint(event.pos):
                    return

main_menu()
