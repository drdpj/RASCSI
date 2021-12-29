# i2c mappings:
# - ssd1307: 0x03c
# - pca9554: 0x3f
#   * io0/pin4=rotary enc a
#   * io1/pin5=rotary enc b
#   * io2/pin6=button 1
#   * io3/pin7=button 2
#   * io4/pin9=button 3
#   * io5/pin10=button 4/rotary button
#   * io6/pin11=led 1
#   * io7/pin12=led 2

import time
import board
import pca9554

from observer import *
from encoder import *

class AttributedButton():
	state = True
	name = "n/a"
	pca_driver = None
	pin = 0

	def __init__(self, pca_driver, pin):
		self.pca_driver = pca_driver
		self.pin = pin

	def read(self):
		return self.pca_driver.read_port(self.pin)


class CtrlBoard(Subject):
	PCA9554_I2C_ADDRESS = 0x3f
	PCA9554_PIN_ENC_A = 1
	PCA9554_PIN_ENC_B = 0
	PCA9554_PIN_BUTTON_1 = 2
	PCA9554_PIN_BUTTON_2 = 3
	PCA9554_PIN_BUTTON_3 = 4
	PCA9554_PIN_BUTTON_ROTARY = 5
	PCA9554_PIN_LED_1 = 6
	PCA9554_PIN_LED_2 = 7

	def __init__(self):
		pca_driver = pca9554.Pca9554(self.PCA9554_I2C_ADDRESS)
                # setup pca9554
		pca_driver.write_config_port(self.PCA9554_PIN_ENC_A, pca9554.INPUT)
		pca_driver.write_config_port(self.PCA9554_PIN_ENC_B, pca9554.INPUT)
		pca_driver.write_config_port(self.PCA9554_PIN_BUTTON_1, pca9554.INPUT)
		pca_driver.write_config_port(self.PCA9554_PIN_BUTTON_2, pca9554.INPUT)
		pca_driver.write_config_port(self.PCA9554_PIN_BUTTON_3, pca9554.INPUT)
		pca_driver.write_config_port(self.PCA9554_PIN_BUTTON_ROTARY, pca9554.INPUT)
		pca_driver.write_config_port(self.PCA9554_PIN_LED_1, pca9554.OUTPUT)
		pca_driver.write_config_port(self.PCA9554_PIN_LED_2, pca9554.OUTPUT)
                
		# button of the rotary encoder
		self.rotary_button = AttributedButton(pca_driver,self.PCA9554_PIN_BUTTON_ROTARY)
		self.rotary_button.state = True
		self.rotary_button.name = "RotBtn"

		# button 1
		self.button1 = AttributedButton(pca_driver,self.PCA9554_PIN_BUTTON_1)
		self.button1.state = True
		self.button1.name = "Bt1"

		# button 2
		self.button2 = AttributedButton(pca_driver,self.PCA9554_PIN_BUTTON_2)
		self.button2.state = True
		self.button2.name = "Bt2"

		# button 3
		self.button3 = AttributedButton(pca_driver,self.PCA9554_PIN_BUTTON_3)
		self.button3.state = True
		self.button3.name = "Bt3"

		# rotary encoder pin a
		self.rotary_a = AttributedButton(pca_driver,self.PCA9554_PIN_ENC_A)
		self.rotary_a.state = True
		self.rotary_a.directionalTransition = False	
		self.rotary_a.name = "RotA"

		# rotary encoder pin b
		self.rotary_b = AttributedButton(pca_driver,self.PCA9554_PIN_ENC_B)
		self.rotary_b.state = True
		self.rotary_b.directionalTransition = False	
		self.rotary_b.name = "RotB"

		self.rotary = Encoder(self.rotary_a, self.rotary_b)
		self.rotary.pos_prev = 0
		self.rotary.name = "Rot"	

	def checkButtonPress(self, button):
		value = button.read()
		if value != button.state and value == False:
			button.state = False
			self.notify(button)
		if value != button.state and value == True:
			button.state = True

	def checkRotaryEncoder(self, rotary):
		rotary.update()
		if self.rotary.pos_prev != self.rotary.pos:
			if (self.rotary.pos/4)%1 == 0:
				self.notify(rotary)
			self.rotary.pos_prev = self.rotary.pos
		
	def processEvents(self):
		self.checkButtonPress(self.rotary_button)
		self.checkButtonPress(self.button1)
		self.checkButtonPress(self.button2)
		self.checkButtonPress(self.button3)
		self.checkRotaryEncoder(self.rotary)
		
