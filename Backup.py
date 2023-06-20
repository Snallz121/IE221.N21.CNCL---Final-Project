import sys
import random 
import pygame
from pygame import mixer
from Game_Object import *
from Game_Define_Variable import *
import os
from utils import load_save, reset_keys

action = {"A": False, "S": False, "D": False, "J": False, "K": False, "L": False} 
COLORCHRG = WHITE
pygame.init() # Khoi chay game

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
        if event.type == pygame.MOUSEBUTTONDOWN and game_page == False:
            pos = event.pos

    # if(pos == None):
    #     pass
    # else:
    #     print("pos:",type(pos))
    print(home_page,difficult_page,option_page,sound_page,game_page)
    if home_page:
        game_window.blit(bg2_img, (0,0)) # Thiết lập background cho game
        game_window.blit(piano_img, (WIDTH // 4, HEIGHT // 8))
        t0 = score_font.render('Start Game', True, COLORCHRG)
        game_window.blit(t0, (WIDTH // 2 - 50, HEIGHT // 2))
        text_x = WIDTH // 2 - 50
        text_y = HEIGHT // 2
        t0_rect = t0.get_rect()
        t0_rect.center = (text_x + t0.get_width() // 2, text_y + t0.get_height() // 2)
        # t0_rect = t0.get_rect(center = (WIDTH // 2 - 25, HEIGHT // 2 - 120))

        t1 = score_font.render('Options', True, COLORCHRG)
        game_window.blit(t1, (WIDTH // 2 - 35, HEIGHT // 2 + 60))
        text_x = WIDTH // 2 - 35
        text_y = HEIGHT // 2 + 60
        t1_rect = t1.get_rect()
        t1_rect.center = (text_x + t1.get_width() // 2, text_y + t1.get_height() // 2)
        # t1_rect = t1.get_rect(center = (WIDTH // 2 - 40, HEIGHT // 2 - 50))

        t2 = score_font.render('Exit Game', True, COLORCHRG)
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
                sys.exit()
            pos = None
    elif difficult_page:
        game_window.blit(bg2_img, (0,0)) # Thiết lập background cho game

        t0 = score_font.render('Easy', True, COLORCHRG)
        game_window.blit(t0, (WIDTH // 2 - 25, HEIGHT // 2 - 150))
        text_x = WIDTH // 2 - 25
        text_y = HEIGHT // 2 - 150
        t0_rect = t0.get_rect()
        t0_rect.center = (text_x + t0.get_width() // 2, text_y + t0.get_height() // 2)

        t1 = score_font.render('Normal', True, COLORCHRG)
        game_window.blit(t1, (WIDTH // 2 - 40, HEIGHT // 2 - 90))
        text_x = WIDTH // 2 - 40
        text_y = HEIGHT // 2 - 90
        t1_rect = t1.get_rect()
        t1_rect.center = (text_x + t1.get_width() // 2, text_y + t1.get_height() // 2)

        t2 = score_font.render('Insane', True, COLORCHRG)
        game_window.blit(t2, (WIDTH // 2 - 35, HEIGHT // 2 - 30))
        text_x = WIDTH // 2 - 35
        text_y = HEIGHT // 2 - 30
        t2_rect = t2.get_rect()
        t2_rect.center = (text_x + t2.get_width() // 2, text_y + t2.get_height() // 2)

        t3 = score_font.render('Return', True, COLORCHRG)
        game_window.blit(t3, (WIDTH // 2 - 35, HEIGHT // 2 + 30))
        text_x = WIDTH // 2 - 35
        text_y = HEIGHT // 2 + 30
        t3_rect = t3.get_rect()
        t3_rect.center = (text_x + t3.get_width() // 2, text_y + t3.get_height() // 2)
        if pos == None:
            pos = pygame.mouse.get_pos()
        else:
            if t0_rect.collidepoint(pos[0], pos[1]) and pygame.mouse.get_pressed()[0]:
                divide_point = 1200
            if t1_rect.collidepoint(pos[0], pos[1]) and pygame.mouse.get_pressed()[0]:
                divide_point = 900
            if t2_rect.collidepoint(pos[0], pos[1]) and pygame.mouse.get_pressed()[0]:
                divide_point = 500
            if t3_rect.collidepoint(pos[0], pos[1]) and pygame.mouse.get_pressed()[0]:
                home_page = True
                difficult_page = False
            pos = None
            if(home_page):
                pass
            else:
                game_page = True 
                difficult_page = False
                x = random.randint(0, 5)
                t = Tile(x * TILE_WIDTH, -TILE_HEIGHT, game_window)
                tile_group.add(t)
    elif option_page:
        pass
    elif game_page:
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