import pygame

import consts


M = 16 # Magic number to create padding from borders in a square


class ChessGui:

	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((consts.WIN_SIZE, consts.WIN_SIZE))
		pygame.display.set_caption('Chess')


	def __del__(self):
		pygame.quit()


	def get_position(self):
		stop = False
		px = py = -1
	
		while not stop:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
					px, py = event.pos
					stop = True
				elif event.type == pygame.QUIT:
					exit()
	
		for i, val in enumerate(range(consts.WIN_SIZE - consts.IMAGE_SIZE, -1, -consts.IMAGE_SIZE)):
			if px > val:
				x = i
				break
	
		for i, val in enumerate(range(consts.WIN_SIZE - consts.IMAGE_SIZE, -1, -consts.IMAGE_SIZE)):
			if py > val:
				y = i
				break
	
		return chr(ord('a') + (consts.CHESS_BOARD_SIZE - x - 1)) + str(y + 1) # Convert point in the window to point in the chess board.


	def draw(self, board, indexes=None):
		'''
		Draw all information.
		`indexes` - List of squares you want to highlight.
		[ (x1, y1, color(r,g,b)), (x2, y2, color(r,g,b)), ... ]
		'''
		self.__draw_board()
	
		if indexes:
			for i in indexes:
				x, y, color = i
				self.__draw_rect(x * consts.IMAGE_SIZE, y * consts.IMAGE_SIZE, consts.IMAGE_SIZE, consts.IMAGE_SIZE, color)
				self.__draw_rect(x * consts.IMAGE_SIZE, y * consts.IMAGE_SIZE, consts.IMAGE_SIZE, consts.IMAGE_SIZE, consts.BLACK, consts.IMAGE_SIZE // 40)
	
		self.__draw_soldiers(board)
	
		pygame.display.update()


	def __get_val(self, board, x, y):
		b = [i.split(' ') for i in str(board).split('\n')] # convert `board` to lists
		val = b[y][x]

		if val == '.':
			return None

		return ('w' if val.isupper() else 'b') + val.lower()


	def __draw_soldiers(self, board):
		for x in range(consts.CHESS_BOARD_SIZE):
			for y in range(consts.CHESS_BOARD_SIZE):
				val = self.__get_val(board, x, y)
				if val == None:
					continue

				path = consts.IMAGES_FOLDER + val + consts.IMAGES_EXTENSION
				img = pygame.image.load(path)
				img = pygame.transform.scale(img, (consts.IMAGE_SIZE * img.get_width() / img.get_height() - M, consts.IMAGE_SIZE - M))
				self.window.blit(img, (x * consts.IMAGE_SIZE + M / 2, y * consts.IMAGE_SIZE + M / 2))


	def __draw_board(self):
		for x in range(0, consts.CHESS_BOARD_SIZE, 2):
			for y in range(0, consts.CHESS_BOARD_SIZE, 2):
				self.__draw_rect(x * consts.IMAGE_SIZE, y * consts.IMAGE_SIZE, consts.IMAGE_SIZE, consts.IMAGE_SIZE, consts.LIGHT_BROWN)
				self.__draw_rect((x + 1) * consts.IMAGE_SIZE, (y + 1) * consts.IMAGE_SIZE, consts.IMAGE_SIZE, consts.IMAGE_SIZE, consts.LIGHT_BROWN)
				self.__draw_rect(x * consts.IMAGE_SIZE, (y + 1) * consts.IMAGE_SIZE, consts.IMAGE_SIZE, consts.IMAGE_SIZE, consts.DARK_BROWN)
				self.__draw_rect((x + 1) * consts.IMAGE_SIZE,  y * consts.IMAGE_SIZE, consts.IMAGE_SIZE, consts.IMAGE_SIZE, consts.DARK_BROWN)


	def __draw_rect(self, x, y, w, h, color, line_width=0):
		'''
		Draw Rectangle.
		(x, y) - The point in the top left corner.
		w - The width of the rectanle.
		h - The height of the rectangle.
		color - (r,g,b)
		line_width - The width of the frame. If `width=0` it draw fill rectancle.
		'''
		pygame.draw.rect(self.window, color, (x, y, w, h), line_width)
