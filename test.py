import pygame 
from Game_Define_Variable import *

def play_mp3(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

file_list = lines# Danh sách tên file mp3

for file_name in file_list:
    file_path = "./Musics/" + file_name + ".mp3"# Đường dẫn đến thư mục chứa file mp3
    play_mp3(file_path)
    input("Press Enter to play the next song...")  # Đợi người dùng nhấn Enter để chạy bài hát tiếp theo
