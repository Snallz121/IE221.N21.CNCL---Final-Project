import sys
import random 
import pygame
from pygame import mixer
from Game_Object import *
from Game_Define_Variable import *
import os
from utils import load_save, reset_keys
from controls import Controls_Handler, DropDown
import PySimpleGUI as sg
pygame.init() # Khoi chay game

actions = {"Col1": False, "Col2": False, "Col3": False, "Col4": False, "Col5": False, "Col6": False, 'Up': False, 'Down': False, 'Action1': False} 
save = load_save()
control_handler = Controls_Handler(save)
canvas = pygame.Surface(Screen_Size)

COLORCHRG = WHITE

def write_file(file, new_content):
    # Open the file in write mode and replace its contents
    new_content = str(new_content)
    with open(file, "w") as file:
        file.write(new_content)

def read_file(file):
    file_path = file # Replace with the actual path to your file
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces
            return int(line)

high_score = read_file(high_score_link)

#Thiet lap game
t = Tile(10, 10, game_window)
x = random.randint(0, 5)
t = Tile(x * TILE_WIDTH, -TILE_HEIGHT, game_window)
tile_group.add(t)
pos = None #Khoi tao vi tri con chuot vua click
playing_music = ""
list1 = DropDown(
    [COLOR_INACTIVE, COLOR_ACTIVE],
    [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
    20, 50, 400, 80, 
    pygame.font.SysFont(None, 30), 
    "Select song at here", lines)
#Vòng lặp của Game
running = True













while running:
    pos = None

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
        write_file(high_score_link, high_score)
        running = False
        sys.exit()
    
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
            write_file(high_score_link, high_score)
            sys.exit()

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE:
                if(option_page):
                    option_page = False
                    home_page = True
                elif(difficult_page):
                    home_page = True
                    difficult_page = False
                elif(select_song_page):
                    select_song_page = False
                    difficult_page = True

            if event.key == control_handler.controls['Col1']:
                pos = points_pos[0]
                if not music_flag:
                    mixer.music.play()
                    music_flag = True
                actions['Col1'] = True
            if event.key == control_handler.controls['Col2']:
                pos = points_pos[1]
                if not music_flag:
                    mixer.music.play()
                    music_flag = True
                actions['Col2'] = True    
            if event.key == control_handler.controls['Col3']:
                pos = points_pos[2]
                if not music_flag:
                    mixer.music.play()
                    music_flag = True
                actions['Col3'] = True    
            if event.key == control_handler.controls['Col4']:
                pos = points_pos[3]
                if not music_flag:
                    mixer.music.play()
                    music_flag = True
                actions['Col4'] = True    
            if event.key == control_handler.controls['Col5']:
                pos = points_pos[4]
                if not music_flag:
                    mixer.music.play()
                    music_flag = True
                actions['Col5'] = True      
            if event.key == control_handler.controls['Col6']:
                pos = points_pos[5]
                if not music_flag:
                    mixer.music.play()
                    music_flag = True
                actions['Col6'] = True      
            if event.key == control_handler.controls['Up']:
                actions['Up'] = True
            if event.key == control_handler.controls['Down']:
                actions['Down'] = True
            if event.key == control_handler.controls['Action1']:
                actions['Action1'] = True

        if event.type == pygame.KEYUP:
            if event.key == control_handler.controls['Col1']:
                actions['Col1'] = False
            if event.key == control_handler.controls['Col2']:
                actions['Col2'] = False   
            if event.key == control_handler.controls['Col3']:
                actions['Col3'] = False   
            if event.key == control_handler.controls['Col4']:
                actions['Col4'] = False   
            if event.key == control_handler.controls['Col5']:
                actions['Col5'] = False      
            if event.key == control_handler.controls['Col6']:
                actions['Col6'] = False  
            if event.key == control_handler.controls['Up']:
                actions['Up'] = False
            if event.key == control_handler.controls['Down']:
                actions['Down'] = False
            if event.key == control_handler.controls['Action1']:
                actions['Action1'] = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and game_page == False and select_song_page == False:
            pos = event.pos















    # if(pos == None):
    #     pass
    # else:
    #     print("pos:",type(pos))
    # print(home_page,difficult_page,option_page,sound_page,game_page)
    if home_page:
        game_window.blit(bg2_img, (0,0)) # Thiết lập background cho game
        game_window.blit(piano_img, (WIDTH // 4, HEIGHT // 8))
        t0 = score_font.render('Start Game', True, (255, 120, 70))
        game_window.blit(t0, (WIDTH // 2 - 50, HEIGHT // 2))
        text_x = WIDTH // 2 - 50
        text_y = HEIGHT // 2
        t0_rect = t0.get_rect()
        t0_rect.center = (text_x + t0.get_width() // 2, text_y + t0.get_height() // 2)
        # t0_rect = t0.get_rect(center = (WIDTH // 2 - 25, HEIGHT // 2 - 120))

        t1 = score_font.render('Options', True, (0, 255, 0))
        game_window.blit(t1, (WIDTH // 2 - 35, HEIGHT // 2 + 60))
        text_x = WIDTH // 2 - 35
        text_y = HEIGHT // 2 + 60
        t1_rect = t1.get_rect()
        t1_rect.center = (text_x + t1.get_width() // 2, text_y + t1.get_height() // 2)
        # t1_rect = t1.get_rect(center = (WIDTH // 2 - 40, HEIGHT // 2 - 50))

        t2 = score_font.render('Exit Game', True, (0, 255, 255))
        game_window.blit(t2, (WIDTH // 2 - 50, HEIGHT // 2 + 120))
        text_x = WIDTH // 2 - 50
        text_y = HEIGHT // 2 + 120
        t2_rect = t2.get_rect()
        t2_rect.center = (text_x + t2.get_width() // 2, text_y + t2.get_height() // 2)

        if pos == None:
            pos = pygame.mouse.get_pos()
        else:
            if t0_rect.collidepoint(pos[0], pos[1]):
                difficult_page = True
                home_page = False
            if t1_rect.collidepoint(pos[0], pos[1]):
                home_page = False
                option_page = True
            if t2_rect.collidepoint(pos[0], pos[1]):
                running = False
                write_file(high_score_link, high_score)
                sys.exit()
            pos = None






    elif difficult_page:
        game_window.blit(bg2_img, (0,0)) # Thiết lập background cho game

        t0 = score_font.render('Easy', True, (255,0,0))
        game_window.blit(t0, (WIDTH // 2 - 25, HEIGHT // 2 - 150))
        text_x = WIDTH // 2 - 25
        text_y = HEIGHT // 2 - 150
        t0_rect = t0.get_rect()
        t0_rect.center = (text_x + t0.get_width() // 2, text_y + t0.get_height() // 2)

        t1 = score_font.render('Normal', True, (0,255,0))
        game_window.blit(t1, (WIDTH // 2 - 40, HEIGHT // 2 - 90))
        text_x = WIDTH // 2 - 40
        text_y = HEIGHT // 2 - 90
        t1_rect = t1.get_rect()
        t1_rect.center = (text_x + t1.get_width() // 2, text_y + t1.get_height() // 2)

        t2 = score_font.render('Insane', True, (0,0,255))
        game_window.blit(t2, (WIDTH // 2 - 35, HEIGHT // 2 - 30))
        text_x = WIDTH // 2 - 35
        text_y = HEIGHT // 2 - 30
        t2_rect = t2.get_rect()
        t2_rect.center = (text_x + t2.get_width() // 2, text_y + t2.get_height() // 2)

        t3 = score_font.render('Return to main menu', True, (255,255,0))
        game_window.blit(t3, (WIDTH // 2 - 100, HEIGHT // 2 + 30))
        text_x = WIDTH // 2 - 100
        text_y = HEIGHT // 2 + 30
        t3_rect = t3.get_rect()
        t3_rect.center = (text_x + t3.get_width() // 2, text_y + t3.get_height() // 2)
        if pos == None:
            pos = pygame.mouse.get_pos()
        else:
            if t0_rect.collidepoint(pos[0], pos[1]) and pygame.mouse.get_pressed()[0]:
                divide_point = 1200
                element_score = 1
            if t1_rect.collidepoint(pos[0], pos[1]) and pygame.mouse.get_pressed()[0]:
                element_score = 2
                divide_point = 800
            if t2_rect.collidepoint(pos[0], pos[1]) and pygame.mouse.get_pressed()[0]:
                element_score = 4
                divide_point = 400
            if t3_rect.collidepoint(pos[0], pos[1]) and pygame.mouse.get_pressed()[0]:
                home_page = True
                difficult_page = False
            pos = None
            if(home_page):
                pass
            else:
                select_song_page = True 
                difficult_page = False
                x = random.randint(0, 5)
                t = Tile(x * TILE_WIDTH, -TILE_HEIGHT, game_window)
                tile_group.add(t)
    
    
    
    
    
    elif select_song_page:
        game_window.blit(bg2_img, (0,0)) # Thiết lập background cho game
        selected_option = list1.update(event_list)
        if selected_option >= 0:
            list1.main = list1.options[selected_option]
        list1.draw(game_window)
        if list1.main != "Select song at here":
            if start_btn.draw(game_window):
                playing_music = "./Musics/" + list1.main + ".mp3"
                mixer.music.load(playing_music)
                game_page = True
                select_song_page = False
    
    
    
    
    
    elif option_page:
        canvas = bg2_img.copy()
        control_handler.render(canvas)
        game_window.blit(pygame.transform.scale(canvas, (Screen_Size[0] * 2,Screen_Size[1] * 2) ), (0,0))
        if return_btn.draw(game_window):
            home_page = True
            option_page = False

    
    
    
    
    
    
    
    
    
    
    elif game_page:
        game_window.blit(bg2_img, (0,0)) # Thiết lập background cho game
        endPointCoordinate = draw_bar(game_window, WIDTH, 2, 7, points) # xác định breakpoint và vẽ các điểm tròn
        """
        Vẽ các kí tự A,S,D,J,K,L ứng với các nút bấm của điểm tròn
        """ 
        A_scene = score_font.render('Col1', True, (255,0,0))
        game_window.blit(A_scene, (TILE_WIDTH - 50, HEIGHT - 150))
        S_scene = score_font.render('Col2', True, (255,0,0))
        game_window.blit(S_scene, (WIDTH // 2 - 125, HEIGHT - 150))
        D_scene = score_font.render('Col3', True, (255,0,0))
        game_window.blit(D_scene, (WIDTH // 2 - 50, HEIGHT - 150))
        J_scene = score_font.render('Col4', True, (255,0,0))
        game_window.blit(J_scene, (WIDTH // 2 + 20, HEIGHT - 150))
        K_scene = score_font.render('Col5', True, (255,0,0))
        game_window.blit(K_scene, (WIDTH // 2 + 90, HEIGHT - 150))
        L_scene = score_font.render('Col6', True, (255,0,0))
        game_window.blit(L_scene, (WIDTH // 2 + 165, HEIGHT - 150))

        # tile_group.update(speed) -- update toc do toan bo dong thoi cac phim nhac
        for tile in tile_group: # update toc do tung phim nhac rieng biet
            tile.update(speed)

            if pos:
                if tile.rect.collidepoint(pos):
                    tile.alive = False
                    score += element_score
                    pos = None
                    if( high_score < score):
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
                write_file(high_score_link, high_score)
                running = False

            if replay_btn.draw(game_window):
                mixer.music.load(playing_music)
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
            
            if home_btn.draw(game_window):
                game_page = False
                home_page = True
                list1 = DropDown(
                [COLOR_INACTIVE, COLOR_ACTIVE],
                [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
                20, 50, 400, 80, 
                pygame.font.SysFont(None, 30), 
                None, lines)
            
            if sound_btn.draw(game_window):
                sound_on = not sound_on
                if sound_on:
                    sound_btn.update_image(sound_on_img)
                    mixer.music.set_volume(0.5)
                else:
                    sound_btn.update_image(sound_off_img)
                    mixer.music.set_volume(0)


    
    
    control_handler.update(actions)            
    clock.tick(FPS)
    pygame.display.update()
    reset_keys(actions)
pygame.quit()