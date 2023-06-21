import pygame

Screen_Size = (WIDTH, HEIGHT) = (432, 768)
TILE_WIDTH = WIDTH // 6
TILE_HEIGHT = 120

#RGB Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
BLUE2 = (2, 239, 239)
PURPLE = (191, 64, 191)

"""
Định nghĩa lớp Tile: Dùng để xác định các thanh đen chạy từ trên xuống dưới, là mục tiêu chính để tăng điểm trong trò chơi và
qui định người chơi phải không được để lọt thanh đen nào qua vạch

Tham số đầu vào: Hoành độ, tung độ của thanh đen, và màn hình trò chơi để vẽ các thanh lên

Trong hàm init chứa các thiết lập giúp xác lập các thuộc tính đối tượng, và đồng thời chứa định nghĩa hình dạng, khung bao quanh đối tượng

Hàm update cập nhật tốc độ của thanh đen khi di chuyển, tỉ lệ thuận với tốc độ hiện tại của trò chơi, bên cạnh đó còn chứa các câu lệnh
giúp render thanh trên màn hình game và trang trí cho thanh 
"""
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, game_window):
        super(Tile, self).__init__()

        self.game_window = game_window
        self.x, self.y = x, y
        self.color = BLACK
        self.alive = True

        self.surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.center = TILE_WIDTH // 2, TILE_HEIGHT // 2 + 15
        self.line_start = self.center[0], self.center[1] + 10
        self.line_end = self.center[0], 20
    
    def update(self, speed):
        self.rect.y += speed
        if self.rect.y >= HEIGHT:
            self.kill()
        if self.alive:
            pygame.draw.rect(self.surface, self.color, (0, 0, TILE_WIDTH, TILE_HEIGHT))
            pygame.draw.rect(self.surface, WHITE, (0, 0, TILE_WIDTH, TILE_HEIGHT), 1)
            pygame.draw.line(self.surface, BLUE, self.line_start, self.line_end, 3)
        else:
            pygame.draw.rect(self.surface, (0,0,0,90), (0, 0, TILE_WIDTH, TILE_HEIGHT))

        self.game_window.blit(self.surface, self.rect)

"""
Định nghĩa lớp Button: Dùng để hiện thực hóa các button vốn không dược lập trình sẵn trong pygame vào trò chơi

Tham số của hàm gồm: hình ảnh của button, tỉ lệ, và hoành, tung độ của button
Hàm draw gúp vẽ đối tượng ra màn hình game, đồng thời, kiểm tra và thực hiện các event của đối tượng
"""
class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()
		
		self.scale = scale
		self.image = pygame.transform.scale(img, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action
