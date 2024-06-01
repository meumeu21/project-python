import pygame
import sys
import random
import os

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Директория с материалами
MATERIALS_DIR = "project_materials"

# Экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Пазлы")

# Шрифты
font_large = pygame.font.SysFont("Comic Sans MS", 36)
font_small = pygame.font.SysFont("Comic Sans MS", 24)

# Таймеры для уровней сложности
TIMER_EASY = 30  # 30 секунд
TIMER_MEDIUM = 120  # 2 минуты
TIMER_HARD = 480  # 8 минут

# Загрузка фонового изображения
background_image_path = os.path.join(MATERIALS_DIR, "background.jpeg")
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Загрузка музыки
music_path = os.path.join(MATERIALS_DIR, "background_music.mp3")
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)  # Зацикливаем фоновую музыку

# Переменные для записи результатов
results = {"easy": None, "medium": None, "hard": None}

# Функция для отрисовки текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Функция для отрисовки текста с белой рамкой (для текста)
def draw_text_with_white_outline(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    # Рисуем белую рамку
    outline = font.render(text, True, WHITE)
    surface.blit(outline, textrect.move(-2, -2))
    surface.blit(outline, textrect.move(2, -2))
    surface.blit(outline, textrect.move(-2, 2))
    surface.blit(outline, textrect.move(2, 2))
    # Рисуем текст поверх рамки
    surface.blit(textobj, textrect)

# Функция для отрисовки текста с черной рамкой (для таймера)
def draw_text_with_black_outline(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    # Рисуем черную рамку
    outline = font.render(text, True, BLACK)
    surface.blit(outline, textrect.move(-2, -2))
    surface.blit(outline, textrect.move(2, -2))
    surface.blit(outline, textrect.move(-2, 2))
    surface.blit(outline, textrect.move(2, 2))
    # Рисуем текст поверх рамки
    surface.blit(textobj, textrect)

# Главное меню
def main_menu():
    music_on = True
    click = False
    while True:
        screen.blit(background_image, (0, 0))  # Отрисовка фонового изображения
        draw_text_with_white_outline("Пазлы", font_large, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        
        mx, my = pygame.mouse.get_pos()
        
        button_start = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25, 300, 50)
        button_music = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 75, 300, 50)
        button_exit = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 175, 300, 50)
        
        if button_start.collidepoint((mx, my)):
            if click:
                difficulty_menu()
                pygame.time.delay(200)  # Задержка 200 миллисекунд
                pygame.event.clear()    # Очистка очереди событий
        if button_music.collidepoint((mx, my)):
            if click:
                if music_on:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                music_on = not music_on
                pygame.time.delay(200)  # Задержка 200 миллисекунд
                pygame.event.clear()    # Очистка очереди событий
        if button_exit.collidepoint((mx, my)):
            pygame.quit()
            sys.exit()
        
        pygame.draw.rect(screen, BLACK, button_start)
        pygame.draw.rect(screen, BLACK, button_music)
        pygame.draw.rect(screen, BLACK, button_exit)
        
        draw_text("Начать игру", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Музыка: Включить" if not music_on else "Музыка: Выключить", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        draw_text("Выйти из игры", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()

# Меню выбора сложности
def difficulty_menu():
    click = False
    while True:
        screen.blit(background_image, (0, 0))  # Отрисовка фонового изображения
        draw_text_with_white_outline("Выберите сложность", font_large, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text_with_white_outline("Правая кнопка мыши - поворот.", font_small, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 60)
        draw_text_with_white_outline("Левая кнопка мыши - выбор двух элементов для обмена.", font_small, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 100)
        
        mx, my = pygame.mouse.get_pos()
        
        button_easy = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 75, 300, 50)
        button_medium = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        button_hard = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 75, 300, 50)
        
        if button_easy.collidepoint((mx, my)):
            if click:
                preview_screen(4, TIMER_EASY, "easy")
        if button_medium.collidepoint((mx, my)):
            if click:
                preview_screen(16, TIMER_MEDIUM, "medium")
        if button_hard.collidepoint((mx, my)):
            if click:
                preview_screen(64, TIMER_HARD, "hard")
        
        pygame.draw.rect(screen, BLACK, button_easy)
        pygame.draw.rect(screen, BLACK, button_medium)
        pygame.draw.rect(screen, BLACK, button_hard)
        
        draw_text("Легко (4 элемента)", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text("Средне (16 элементов)", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25)
        draw_text("Сложно (64 элемента)", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()

# Экран проигрыша
def lose_screen():
    click = False
    while True:
        screen.fill(WHITE)
        draw_text("Вы проиграли!", font_large, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        
        mx, my = pygame.mouse.get_pos()
        
        button_exit = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        
        if button_exit.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        
        pygame.draw.rect(screen, BLACK, button_exit)
        
        draw_text("Выйти из игры", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25)
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()

# Экран выигрыша
def win_screen(difficulty, seconds):
    results[difficulty] = seconds
    click = False
    while True:
        screen.fill(WHITE)
        draw_text("Вы выиграли!", font_large, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text(f"Ваше время: {seconds} секунд", font_small, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 50)
        
        mx, my = pygame.mouse.get_pos()
        
        button_exit = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        
        if button_exit.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        
        pygame.draw.rect(screen, BLACK, button_exit)
        
        draw_text("Выйти из игры", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25)
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()

# Экран предварительного просмотра
def preview_screen(pieces, timer, difficulty):
    images = load_images()
    original_image = random.choice(images)
    original_image = pygame.transform.scale(original_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    click = False
    while True:
        screen.blit(original_image, (0, 0))  # Отрисовка полной картинки
        
        mx, my = pygame.mouse.get_pos()
        
        button_continue = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100, 300, 50)
        
        if button_continue.collidepoint((mx, my)):
            if click:
                start_game_with_preview(original_image, pieces, timer, difficulty)
                pygame.time.delay(200)  # Задержка 200 миллисекунд
                pygame.event.clear()    # Очистка очереди событий
        
        pygame.draw.rect(screen, BLACK, button_continue)
        
        draw_text("Продолжить", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75)
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()

# Функция для начала игры с предварительным просмотром
def start_game_with_preview(original_image, pieces, timer, difficulty):
    puzzle_pieces = create_puzzle(original_image, pieces)
    game_loop(puzzle_pieces, original_image, timer, difficulty)

# Загрузка изображений из папки
def load_images():
    images = []
    images_dir = os.path.join(MATERIALS_DIR, "images")
    for filename in os.listdir(images_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img = pygame.image.load(os.path.join(images_dir, filename))
            images.append(img)
    return images

# Создание пазлов
def create_puzzle(original_image, pieces):
    img = original_image
    
    puzzle_pieces = []
    grid_size = int(pieces ** 0.5)
    piece_width = SCREEN_WIDTH // grid_size
    piece_height = SCREEN_HEIGHT // grid_size
    
    positions = [(x, y) for x in range(0, SCREEN_WIDTH, piece_width) for y in range(0, SCREEN_HEIGHT, piece_height)]
    random.shuffle(positions)
    
    for i in range(pieces):
        x = (i % grid_size) * piece_width
        y = (i // grid_size) * piece_height
        piece = img.subsurface((x, y, piece_width, piece_height))
        angle = random.choice([0, 90, 180, 270])
        piece = pygame.transform.rotate(piece, angle)
        rect = piece.get_rect(topleft=positions[i])
        puzzle_pieces.append({"image": piece, "rect": rect, "angle": angle, "correct_pos": (x, y)})
    
    return puzzle_pieces

# Игровой цикл
def game_loop(puzzle_pieces, original_image, game_time, difficulty):
    selected_piece = None
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    while True:
        screen.fill(WHITE)
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        if seconds >= game_time:
            lose_screen()

        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for piece in puzzle_pieces:
                        if piece["rect"].collidepoint((mx, my)):
                            if selected_piece is None:
                                selected_piece = piece
                            else:
                                piece["rect"].topleft, selected_piece["rect"].topleft = selected_piece["rect"].topleft, piece["rect"].topleft
                                selected_piece = None
                            break
                if event.button == 3:
                    for piece in puzzle_pieces:
                        if piece["rect"].collidepoint((mx, my)):
                            piece["angle"] = (piece["angle"] + 90) % 360
                            piece["image"] = pygame.transform.rotate(piece["image"], 90)
                            break

        draw_puzzle(puzzle_pieces)
        draw_text_with_black_outline(f"Время: {game_time - seconds}", font_small, WHITE, screen, 700, 20)

        pygame.display.update()
        clock.tick(30)

        # Проверка, решен ли пазл
        if check_puzzle_solved(puzzle_pieces):
            win_screen(difficulty, seconds)

# Отрисовка пазлов
def draw_puzzle(puzzle_pieces):
    for piece in puzzle_pieces:
        screen.blit(piece["image"], piece["rect"])

# Проверка, решен ли пазл
def check_puzzle_solved(puzzle_pieces):
    for piece in puzzle_pieces:
        if piece["rect"].topleft != piece["correct_pos"] or piece["angle"] != 0:
            return False
    return True

# Запуск главного меню
main_menu()
