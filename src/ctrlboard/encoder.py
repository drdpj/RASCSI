import time

class Encoder():
	def __init__(self, A, B):
		self.A = A
		self.B = B
		self.pos = 0
		self.scaled_pos = 0
		self.state = 0
		self.direction = 0
		self.detent_counter = 0
	
		value_enc_a = self.A.read()
		value_enc_b = self.B.read()

		if value_enc_a:
			self.state |= 0b0001
		if value_enc_b:
			self.state |= 0b0010

	def update(self):
		value_enc_a = self.A.read()
		value_enc_b = self.B.read()

		self.direction = 0
		state = self.state & 0b0011
		if value_enc_a:
			state |= 0b0100
		if value_enc_b:
			state |= 0b1000

		self.state = state >> 2

		if state == 0b0001 or state == 0b0111 or state == 0b1000 or state == 0b1110:
			self.pos += 1
			self.direction = 1
		elif state == 0b0010 or state == 0b0100 or state == 0b1011 or state == 0b1101:
			self.pos -= 1
			self.direction = -1
		elif state == 0b0011 or state == 0b1100:
			self.pos += 2
			self.direction = 1
		elif state == 0b0110 or state == 0b1001:
			self.pos -= 2
			self.direction = -1

		self.scaled_pos = int(self.pos / 4)
