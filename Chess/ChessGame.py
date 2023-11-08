import chess
import pymsgbox

import ChessGui
import consts


class ChessGame:
	def __init__(self):
		self.board = chess.Board()
		self.gui = ChessGui.ChessGui()


	def run(self):
		self.current_player_color = 'w'

		while True:
			self.make_move()

			if self.board.is_check():
				self.gui.draw(self.board)
				if self.board.is_checkmate():
					won_color = 'white' if self.current_player_color == 'w' else 'black'
					pymsgbox.alert(f'the {won_color} player won', 'checkmate')
					exit()
				else:
					threatened_color = 'black' if self.current_player_color == 'w' else 'white'
					pymsgbox.alert(f'the {threatened_color} player is threatened', 'check')

			self.current_player_color = 'b' if self.current_player_color == 'w' else 'w'
			

	def make_move(self):
		while True:
			self.gui.draw(self.board)

			# choose source
			val = None
			while val == None or val[1] != self.current_player_color:
				src = self.gui.get_position()
				val = self.get_board_val(src)
				

			change = False # change the pawn at board end

			# mark valid moves
			idx = [] # format: [ ( x, y, (r,g,b) ), ... ]
			for i in self.board.legal_moves:
				i_str = str(i)
				if src == i_str[:2]:
					pos = i_str[2:]

					if len(pos) == 3:
						pos = pos[:-1]
						change = True

					val = self.get_board_val(pos)
					mark_color = consts.RED if val else consts.BLUE

					idx += [ list(self.get_index(pos)) + [mark_color] ]

			idx += [ list(self.get_index(src)) + [consts.GREEN] ]
			self.gui.draw(self.board, idx) # Draws the board and highlights the selected square with the legal moves

			# choose destination
			dst = self.gui.get_position()
			val = self.get_board_val(dst)
			
			if (src == dst) or (val != None and val[1] == self.current_player_color and dst != src):
				continue # need to select `src` and `dst` again because the `dst` is invalid

			c = ''
			if change:
				c = input ('enter your new tool (q/r/b/n): ')
				while c not in ['q','r','b','n']:
					c = input ('enter your new tool (q/r/b/n): ')

			move = chess.Move.from_uci(src + dst + c)
			if move not in self.board.legal_moves:
				continue

			if src != dst:
				self.board.push(move)
				break


	def get_index(self, pos):
		# `pos` example: 'a2', 'g5'
		# return: (x, y) in graphical board

		x = ord(pos[0]) - ord('a')
		y = consts.CHESS_BOARD_SIZE - int(pos[1])
		return x, y

	def get_board_val(self, pos):
		# `pos` example: 'a2', 'g5'
		# return: name, color
		# if returns `None` it means that `pos` is empty

		x, y = self.get_index(pos)
		b = [i.split(' ') for i in str(self.board).split('\n')] # convert `board` to lists
		val = b[y][x]
		if val == '.':
			return None
		return val.lower(), 'w' if val.isupper() else 'b'
