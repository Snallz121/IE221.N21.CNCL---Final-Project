import sys
import random 
import pygame
from pygame import mixer
from Game_Object import *
import os
pygame.init() # Khoi chay game

#Game Stat
info = pygame.display.Info()
width = info.current_w
height = info.current_h
Screen_Size = (WIDTH, HEIGHT) = (432, 768)
TILE_WIDTH = WIDTH // 6
TILE_HEIGHT = 120
clock = pygame.time.Clock()
FPS = 30
endPointCoordinate = None

#RGB Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
BLUE2 = (2, 239, 239)
PURPLE = (191, 64, 191)

# Game Image
Background_image = pygame.image.load('Assets/bg.png')
Background_image = pygame.transform.scale(Background_image, Screen_Size)

bg2_img = pygame.image.load('Assets/bg2.png')
bg2_img = pygame.transform.scale(bg2_img, (WIDTH, HEIGHT))

piano_img = pygame.image.load('Assets/piano.png')
piano_img = pygame.transform.scale(piano_img, (212, 212))

title_img = pygame.image.load('Assets/title.png')
title_img = pygame.transform.scale(title_img, (200, 50))

start_img = pygame.image.load('Assets/start.png')
start_img = pygame.transform.scale(start_img, (140, 60))
start_rect = start_img.get_rect(center=(WIDTH//2, HEIGHT // 2 + 60))

overlay = pygame.image.load('Assets/red overlay.png')
overlay = pygame.transform.scale(overlay, (WIDTH, HEIGHT))

option_img = pygame.image.load('Assets/option.png')
option_img = pygame.transform.scale(option_img, (120, 40))
option_rect = start_img.get_rect(center=(WIDTH//2, HEIGHT-100))

close_img = pygame.image.load('Assets/closeBtn.png')
replay_img = pygame.image.load('Assets/replay.png')
difficult_img = pygame.image.load("Assets/difficult.png")

close_btn = Button(close_img, (24, 24), WIDTH // 4 - 18, HEIGHT//2 + 120)
replay_btn = Button(replay_img, (36,36), WIDTH // 2  - 18, HEIGHT//2 + 115)
difficult_btn = Button(difficult_img, (36, 36), WIDTH - WIDTH // 4 - 18, HEIGHT//2 + 120)

#font game 
score_font = pygame.font.Font('Fonts/Futura condensed.ttf', 32)

#Thiết lập kích cỡ màn hình game
if width >= height:
    game_window = pygame.display.set_mode(Screen_Size, pygame.NOFRAME)
else:
    game_window = pygame.display.set_mode(Screen_Size, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN | pygame.RESIZABLE)

#Cac ham support cho game
def get_speed(score): # Hàm kiểm soát tốc độ các phím trong game
    return 200 + 5 * score

""""
Hàm drawbar với các tham số đầu vào gồm: màn hình game, chiều rộng của thanh, chiều dài của thanh, bán kính điểm tròn,
cùng với points là 1 mảng 0 có số lượng phần tử ứng với số phím dùng để thao tác trong game trừ chuột

Return Tung độ của thanh giới hạn -- Mục đích để thuận tiện hơn cho việc xét điều kiện dừng / game over của trò chơi
"""
def draw_bar(screen, bar_width, bar_height, point_radius, points):
    # Vẽ thanh ngang
    bar_x = (screen.get_width() - screen.get_width()//4) * 0
    bar_y = (screen.get_height() - screen.get_height()//4)
    pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

    # Vẽ các điểm
    num_points = len(points)
    point_spacing = bar_width // (num_points)

    point_y = bar_y + bar_height // 2
    point_x = 40
    for i, point in enumerate(points):
        pygame.draw.circle(screen, (255, 140, 70), (point_x, point_y), point_radius)
        points_pos.append((point_x, point_y))
        point_x += point_spacing
    return bar_y

#Group cac object trong Game
tile_group = pygame.sprite.Group()

#Đọc danh sách bài hát
music_folder = "./Musics/"
music_files = os.listdir(music_folder)

#Thiết lập âm thanh cho Game
mixer.init()
k = random.randint(0, len(music_files) - 1)
music_file = os.path.join(music_folder, music_files[k])  # Choose the first file in the list
mixer.music.load(music_file)
music_flag = False
buzzer_fx = pygame.mixer.Sound('Sounds/piano-buzzer.mp3')

#Thiet lap cac tham so trong game
speed = 2
num_tile = 1
score = 0
points = [0, 0, 0, 0, 0, 0]
points_pos = []
game_over = False
high_score = 0
divide_point = 1200

#Thiết lập các biến đại diện cho các màn hình
home_page = True
option_page = True
difficult_page = False
game_page = False

#Thiet lap game
t = Tile(10, 10, game_window)
x = random.randint(0, 5)
t = Tile(x * TILE_WIDTH, -TILE_HEIGHT, game_window)
tile_group.add(t)
pos = None #Khoi tao vi tri con chuot vua click
#Vòng lặp của Game
running = True
while running:
    pos = None
     # Thiết lập background cho game

    """
    Xử lí và bắt các event xuất hiện trong trò chơi

    Hàm for ở dòng 158 giúp chúng ta bắt các sự kiện ngay tại thời điểm event xuất hiện

    Ở đây để thoát ra khỏi trò chơi, tổ hợp phím Ctrl + F4 hay esc giúp chúng ta thoát khỏi và tắt màn hinh trò chơi

    Trong khi đó A,S,D,J.K,L là các tổ hợp phím để tương tác với các phím nhạc trong game, khi nhấn các phím sẽ diễn ra các sự kiện,
    các sự kiện sẽ được xét giữa điểm tròn trên đường kẻ mốc và thanh nhạc, khi nhấn các phím mầ thanh nhạc chưa đến trò chơi sẽ kết thúc
    ngay lập tức và điểm số sẽ được lưu lại sau đó.

    Ngoài ra ta còn có bắt sự kiện click chuột, khi click chuột tọa độ nơi con trỏ chuột sẽ được lưu lại và được xử lí, nếu chúng phù hợp
    trong trường hợp ở đây là các phím nhạc và các button, option ở màn hình chọn độ khó, chương trình sẽ thực hiện chúng sau đó, 
    như thiết lập độ khó 
    """
    all_keys = pygame.key.get_pressed()

    if all_keys[pygame.K_F4] and (all_keys[pygame.K_LCTRL] or all_keys[pygame.K_RCTRL]):
        running = False
        sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False
                sys.exit()
            if event.key == pygame.K_a:
                pos = points_pos[0]
                if not music_flag:
                    mixer.music.play()
                    music_flag = True
            if event.key == pygame.K_s:
                pos = points_pos[1]
                if not music_flag:
                    mixer.music.play()
                    music_flag = True 
            if event.key == pygame.K_d:
                pos = points_pos[2]
                if not music_flag:
                    mixer.music.play()
                    music_flag = True 
            if event.key == pygame.K_j:
               pos = points_pos[3]
               if not music_flag:
                    mixer.music.play()
                    music_flag = True  
            if event.key == pygame.K_k:
                pos = points_pos[4]
                if not music_flag:
                    mixer.music.play()
                    music_flag = True   
            if event.key == pygame.K_l:
                pos = points_pos[5]
                if not music_flag:
                    mixer.music.play()
                    music_flag = True        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

    # if(pos == None):
    #     pass
    # else:
    #     print("pos:",type(pos))

    if home_page:
        game_window.blit(Background_image, (0,0)) # Thiết lập background cho game
        game_window.blit(piano_img, (WIDTH // 4, HEIGHT // 8))
        game_window.blit(start_img, start_rect)

        if pos and start_rect.collidepoint(pos):
            home_page = False
            difficult_page = True
            pos = None
    if option_page:
        pass 
    if difficult_page:
        game_window.blit(bg2_img, (0,0)) # Thiết lập background cho game

        t0 = score_font.render('Easy', True, WHITE)
        game_window.blit(t0, (WIDTH // 2 - 25, HEIGHT // 2 - 120))
        text_x = WIDTH // 2 - 25
        text_y = HEIGHT // 2 - 120
        t0_rect = t0.get_rect()
        t0_rect.center = (text_x + t0.get_width() // 2, text_y + t0.get_height() // 2)
        # t0_rect = t0.get_rect(center = (WIDTH // 2 - 25, HEIGHT // 2 - 120))

        t1 = score_font.render('Normal', True, WHITE)
        game_window.blit(t1, (WIDTH // 2 - 40, HEIGHT // 2 - 50))
        text_x = WIDTH // 2 - 40
        text_y = HEIGHT // 2 - 50
        t1_rect = t1.get_rect()
        t1_rect.center = (text_x + t1.get_width() // 2, text_y + t1.get_height() // 2)
        # t1_rect = t1.get_rect(center = (WIDTH // 2 - 40, HEIGHT // 2 - 50))

        t2 = score_font.render('Insane', True, WHITE)
        game_window.blit(t2, (WIDTH // 2 - 35, HEIGHT // 2 + 20))
        text_x = WIDTH // 2 - 35
        text_y = HEIGHT // 2 + 20
        t2_rect = t2.get_rect()
        t2_rect.center = (text_x + t2.get_width() // 2, text_y + t2.get_height() // 2)
        # t2_rect = t2.get_rect(center = (WIDTH // 2 - 35, HEIGHT // 2 + 20))

        if pos == None:
            pos = pygame.mouse.get_pos()
        else:
            if t0_rect.collidepoint(pos[0], pos[1]):
                divide_point = 1200
            if t1_rect.collidepoint(pos[0], pos[1]):
                divide_point = 900
            if t2_rect.collidepoint(pos[0], pos[1]):
                divide_point = 500
            pos = None
            game_page = True 
            difficult_page = False
            x = random.randint(0, 5)
            t = Tile(x * TILE_WIDTH, -TILE_HEIGHT, game_window)
            tile_group.add(t)

    if game_page:
        game_window.blit(Background_image, (0,0)) # Thiết lập background cho game
        endPointCoordinate = draw_bar(game_window, WIDTH, 2, 7, points) # xác định breakpoint và vẽ các điểm tròn
        """
        Vẽ các kí tự A,S,D,J,K,L ứng với các nút bấm của điểm tròn
        """ 
        A_scene = score_font.render('A', True, (255,0,0))
        game_window.blit(A_scene, (TILE_WIDTH - 40, HEIGHT - 150))
        S_scene = score_font.render('S', True, (255,0,0))
        game_window.blit(S_scene, (WIDTH // 2 - 110, HEIGHT - 150))
        D_scene = score_font.render('D', True, (255,0,0))
        game_window.blit(D_scene, (WIDTH // 2 - 38, HEIGHT - 150))
        J_scene = score_font.render('J', True, (255,0,0))
        game_window.blit(J_scene, (WIDTH // 2 + 35, HEIGHT - 150))
        K_scene = score_font.render('K', True, (255,0,0))
        game_window.blit(K_scene, (WIDTH // 2 + 105, HEIGHT - 150))
        L_scene = score_font.render('L', True, (255,0,0))
        game_window.blit(L_scene, (WIDTH // 2 + 180, HEIGHT - 150))

        # tile_group.update(speed) -- update toc do toan bo dong thoi cac phim nhac
        for tile in tile_group: # update toc do tung phim nhac rieng biet
            tile.update(speed)

            if pos:
                if tile.rect.collidepoint(pos):
                    tile.alive = False
                    score += 1
                    pos = None
                    if( high_score > score):
                        high_score = score 

            if (tile.rect.top >= endPointCoordinate) and tile.alive:
                if not game_over:
                    game_over = True
        
        if pos:
            game_over = True        
        
        if len(tile_group) > 0:
            t = tile_group.sprites()[-1]
            if t.rect.top + speed >= 0:
                x = random.randint(0, 5)
                y = -TILE_HEIGHT - (0 - t.rect.top)
                t = Tile(x * TILE_WIDTH, y, game_window)
                tile_group.add(t)
                num_tile += 1
        
        img1 = score_font.render(f'Score : {score}', True, WHITE)
        game_window.blit(img1, (70 - img1.get_width() / 2, 25))
        img2 = score_font.render(f'High : {high_score}', True, WHITE)
        game_window.blit(img2, (340 - img2.get_width() / 2, 25))
        
        speed = get_speed(score) * FPS / divide_point
        
        if game_over:
            speed = 0
            game_window.blit(overlay, (0,0))
            mixer.music.stop()

            if close_btn.draw(game_window):
                running = False
            if replay_btn.draw(game_window):
                k = random.randint(0, len(music_files) - 1)
                music_file = os.path.join(music_folder, music_files[k])  # Choose the first file in the list
                mixer.music.load(music_file)

                tile_group.empty()
                score = 0
                speed = 2
                game_over = False
                music_flag = False
                x = random.randint(0, 5)
                t = Tile(x * TILE_WIDTH, -TILE_HEIGHT, game_window)
                tile_group.add(t)

            if difficult_btn.draw(game_window):
                difficult_page = True
                game_page = False
                game_over = False
                music_flag = False
                tile_group.empty()
                score = 0
                speed = 2
                
    clock.tick(FPS)
    pygame.display.update()
pygame.quit()