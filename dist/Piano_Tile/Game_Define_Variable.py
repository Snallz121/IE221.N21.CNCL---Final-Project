import pygame
from pygame import mixer, font
from Game_Object import Button
import random
import os
#Game Stat
pygame.init()
Screen_Size = (WIDTH, HEIGHT) = (432, 768)
TILE_WIDTH = WIDTH // 6
TILE_HEIGHT = 120
clock = pygame.time.Clock()
FPS = 30
endPointCoordinate = None
high_score_link = "./high_score.txt"

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
return_img = pygame.image.load("Assets/return.png")
sound_off_img = pygame.image.load("Assets/soundOffBtn.png")
sound_on_img = pygame.image.load("Assets/soundOnBtn.png")
home_img = pygame.image.load('Assets/home.png')

close_btn = Button(close_img, (24, 24), WIDTH // 4 - 18, HEIGHT//2 + 120)
replay_btn = Button(replay_img, (36,36), WIDTH // 2  - 18, HEIGHT//2 + 115)
difficult_btn = Button(difficult_img, (48, 48), WIDTH - WIDTH // 4 - 18, HEIGHT//2 + 110)
start_btn = Button(start_img, (144,72), WIDTH // 2 - 60, HEIGHT//2 + 115)
return_btn = Button(return_img, (36, 36), 10, 40)
sound_btn = Button(sound_on_img, (48, 48), WIDTH // 2 + 20, HEIGHT//2 + 180)
home_btn = Button(home_img, (48, 48), WIDTH // 2  - 60, HEIGHT//2 + 180)

#font game 
score_font = font.Font('./Fonts/Futura condensed.ttf', 32)

#Thiết lập kích cỡ màn hình game
game_window = pygame.display.set_mode(Screen_Size, pygame.NOFRAME)

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
divide_point = 1200
high_score = 0
element_score = 1

#Thiết lập các biến đại diện cho các màn hình
home_page = True
difficult_page = False
select_song_page = False
option_page = False
sound_page = False
game_page = False
sound_on = True

#
COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)

#Read song list
file_path = "./SongNameList.txt"  # Replace with the actual path to your file

lines = []

with open(file_path, "r") as file:
    for line in file:
        line = line.strip()  # Remove leading/trailing whitespaces
        lines.append(line)