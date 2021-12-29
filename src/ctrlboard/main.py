# pip install smbus
import time
import observer
import Adafruit_SSD1306

from typing import List
from ctrlboard import AttributedButton, CtrlBoard
from encoder import Encoder

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class ButtonPressPrinter(observer.Observer):
	def update(self, updatedObject):
		if isinstance(updatedObject, AttributedButton):
			print(updatedObject.name + " has been pressed!")
		if isinstance(updatedObject, Encoder):	
			print(updatedObject.scaled_pos)

#class CtrlBoardHandler(observer.Observer):
#	def update(self, updatedObject):
#		if isinstance(updatedObject, AttributedButton):
#			print(updatedObject.name + " has been pressed!")
#		if isinstance(updatedObject, Encoder):	
#			print(updatedObject.direction)

class Menu:
	_entries: List = []
	_item_selection = 0

	def addEntry(self, text):
		self._entries.append(text)

class MenuRenderer():
	message = ""

	def __init__(self, menu):
		self.menu = menu
		self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
		self.disp.begin()
		self.disp.clear()
		self.disp.display()
		self.image = Image.new('1', (self.disp.width, self.disp.height))
		self.draw = ImageDraw.Draw(self.image)	

		#self.font = ImageFont.truetype('fonts/DejaVuSansMono-Bold.ttf', 12)
		self.font = ImageFont.truetype('fonts/SourceCodePro-Bold.ttf', 12)
	
	def render(self):
		i = 0
		padding = -2
		top = padding
		x = 0
		
		self.disp.clear()
		if self.message != "":
			self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=255)
			self.draw.text((x, top + 2*12), self.message, font=self.font, stroke_fill=0, fill=0, textsize=20)			
			self.disp.image(self.image)
			self.disp.display()
			return

		self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
		for menuEntry in self.menu._entries:
			if (i == self.menu._item_selection):
				self.draw.rectangle((x, top+i*12, self.disp.width, top+(i+1)*12), outline=0, fill=255)
				self.draw.text((x, top + i*12), menuEntry, font=self.font, stroke_fill=0, fill=0, textsize=20)
			else:
				self.draw.text((x, top + i*12), menuEntry, font=self.font, stroke_fill=0, fill=255, textsize=20)

			i += 1			

		self.disp.image(self.image)
		self.disp.display()

class CtrlBoardMenuRenderer(MenuRenderer, observer.Observer):
	def update(self, updatedObject):
		if isinstance(updatedObject, AttributedButton):
			print(updatedObject.name + " has been pressed!")
			self.message = updatedObject.name + " pressed!"
			self.render()
			time.sleep(1)
			self.message = ""
			self.render()
		if isinstance(updatedObject, Encoder):	
#			print(updatedObject.direction)
			if updatedObject.direction == 1:
				self.menu._item_selection += 1
			if updatedObject.direction == -1:
				self.menu._item_selection -= 1
			self.render()


#############################################
# Main
#############################################


ctrlboard = CtrlBoard()
buttonPressPrinter = ButtonPressPrinter()
ctrlboard.attach(buttonPressPrinter)

menu = Menu()
menu.addEntry("Hello")
menu.addEntry("Foo")
menu.addEntry("Bar")
menu.addEntry("This")
menu.addEntry("is")
#menu.addEntry("a")
#menu.addEntry("test")

#menuRenderer = MenuRenderer(menu)
menuRenderer = CtrlBoardMenuRenderer(menu)
ctrlboard.attach(menuRenderer)

menuRenderer.render()
while True:
    ctrlboard.processEvents()



