import pygame, sys
from utils import write_save

# Khai báo kích thước màn hình
WIDTH = 432
HEIGHT = 768
Screen_Size = (WIDTH, HEIGHT)
"""
Lớp Controls_Handler để quản lý các nút trên bàn phím, xử lí các sự kiện liên quan tới các nút trên bàn phím

Phương thức khởi tạo init nhận tham số đầu vào là dữ liệu từ file json


-Phương thức update để cập nhật lại sau mỗi lần một event được thực thi
-Phương thức render để vẽ giao diện lên màn hình
-Phương thức navigate menu giúp ta di chuyển thanh đánh dấu và chọn mục ta muốn chọn
-Phương thức set_new_control dùng để thay thế phím sẽ được dùng để tương tác trong trò chơi, 
ngoài ra nó còn ngăn sẽ không có phím nào trùng lặp trong trò chơi 
- Phương thức display_control vẽ lên màn hình các cài đặt của phím điều khiển hiện tại
- Phương thức setup thiết lập các cài đặt ban đầu cho đối tượng
- Phương thức draw_text giúp vẽ và thiết lập các tương tác của chữ lên giao diện

"""
class Controls_Handler:
    def __init__(self, save):
        self.save_file = save
        self.curr_block = save["current_profile"]
        self.controls = self.save_file["controls"][str(self.curr_block)]
        self.setup()
    
    def update(self, actions):
        if self.selected: self.set_new_control()
        else: self.navigate_menu(actions)
    
    def render(self, surface):
        self.draw_text(surface, "Control Profile", 32, pygame.Color((255, 0, 0)),
                    WIDTH // 16 + 80 ,HEIGHT // 16)
        self.display_controls(surface, self.save_file['controls'][str(self.curr_block)])
        # if self.curr_block == self.save_file["current_profile"]:
        #     self.draw_text(surface, "*", 30, pygame.Color((0, 0, 0)), 10, 40)

    def navigate_menu(self, actions):
        #Move the cursor up and down
        if actions["Down"]: self.curr_index = (self.curr_index + 1) % (len(self.save_file["controls"][str(self.curr_block)]) + 1)
        if actions["Up"]: self.curr_index = (self.curr_index - 1) % (len(self.save_file["controls"][str(self.curr_block)]) + 1)

        if actions["Action1"]:
            self.selected = True

    def set_new_control(self):
        selected_control = self.cursor_dict[self.curr_index]
        done = False
        while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            done = True
                            pygame.quit()
                            sys.exit()
                        elif event.key not in self.save_file["controls"][str(self.curr_block)].values():
                            self.save_file["controls"][str(self.curr_block)][selected_control] = event.key
                            write_save(self.save_file)
                            self.selected = False
                            done = True

    def display_controls(self, surface, controls):
        color = (255, 0, 0) if self.selected else (255, 250, 239)
        pygame.draw.rect(surface, color, (48, HEIGHT // 8 + (self.curr_index * 30), 120, 20))
        i = 0
        for control in controls:
            self.draw_text(surface, control + " - " + pygame.key.name(controls[control]), 20,
                        pygame.Color(0, 0, 0), WIDTH // 16 + 80 ,HEIGHT // 9 + 20+ i)
            i += 30
        self.draw_text(surface, "Return", 20, pygame.Color((0, 0, 0)), WIDTH // 16 + 80 ,HEIGHT // 9 + 20 + i)

    def setup(self):
        self.selected = False
        self.font = pygame.font.Font('./Fonts/Futura condensed.ttf', 32)
        self.cursor_dict = {}
        self.curr_index = 0
        i = 0 
        for control in self.controls:
            self.cursor_dict[i] = control
            i += 1
        self.cursor_dict[i] = "Set"
    
    def draw_text(self, surface, text, size, color, x, y):
        font = pygame.font.Font('./Fonts/Futura condensed.ttf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

class DropDown():

    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1