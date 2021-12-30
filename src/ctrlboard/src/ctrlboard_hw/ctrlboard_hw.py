from ctrlboard_hw import pca9554
from ctrlboard_hw.attributed_button import AttributedButton
from ctrlboard_hw.ctrlboard_hw_constants import CtrlBoardHardwareConstants
from ctrlboard_hw.encoder import Encoder
from observer import Subject


class CtrlBoardHardware(Subject):

    def __init__(self):
        pca_driver = pca9554.Pca9554(CtrlBoardHardwareConstants.PCA9554_I2C_ADDRESS)
        # setup pca9554
        pca_driver.write_config_port(CtrlBoardHardwareConstants.PCA9554_PIN_ENC_A, pca9554.INPUT)
        pca_driver.write_config_port(CtrlBoardHardwareConstants.PCA9554_PIN_ENC_B, pca9554.INPUT)
        pca_driver.write_config_port(CtrlBoardHardwareConstants.PCA9554_PIN_BUTTON_1, pca9554.INPUT)
        pca_driver.write_config_port(CtrlBoardHardwareConstants.PCA9554_PIN_BUTTON_2, pca9554.INPUT)
        pca_driver.write_config_port(CtrlBoardHardwareConstants.PCA9554_PIN_BUTTON_3, pca9554.INPUT)
        pca_driver.write_config_port(CtrlBoardHardwareConstants.PCA9554_PIN_BUTTON_ROTARY, pca9554.INPUT)
        pca_driver.write_config_port(CtrlBoardHardwareConstants.PCA9554_PIN_LED_1, pca9554.OUTPUT)
        pca_driver.write_config_port(CtrlBoardHardwareConstants.PCA9554_PIN_LED_2, pca9554.OUTPUT)

        # button of the rotary encoder
        self.rotary_button = AttributedButton(pca_driver, CtrlBoardHardwareConstants.PCA9554_PIN_BUTTON_ROTARY)
        self.rotary_button.state = True
        self.rotary_button.name = "RotBtn"

        # button 1
        self.button1 = AttributedButton(pca_driver, CtrlBoardHardwareConstants.PCA9554_PIN_BUTTON_1)
        self.button1.state = True
        self.button1.name = "Bt1"

        # button 2
        self.button2 = AttributedButton(pca_driver, CtrlBoardHardwareConstants.PCA9554_PIN_BUTTON_2)
        self.button2.state = True
        self.button2.name = "Bt2"

        # button 3
        self.button3 = AttributedButton(pca_driver, CtrlBoardHardwareConstants.PCA9554_PIN_BUTTON_3)
        self.button3.state = True
        self.button3.name = "Bt3"

        # rotary encoder pin a
        self.rotary_a = AttributedButton(pca_driver, CtrlBoardHardwareConstants.PCA9554_PIN_ENC_A)
        self.rotary_a.state = True
        self.rotary_a.directionalTransition = False
        self.rotary_a.name = "RotA"

        # rotary encoder pin b
        self.rotary_b = AttributedButton(pca_driver, CtrlBoardHardwareConstants.PCA9554_PIN_ENC_B)
        self.rotary_b.state = True
        self.rotary_b.directionalTransition = False
        self.rotary_b.name = "RotB"

        self.rotary = Encoder(self.rotary_a, self.rotary_b)
        self.rotary.pos_prev = 0
        self.rotary.name = "Rot"

    def check_button_press(self, button):
        value = button.read()
        if value != button.state and value == 0:
            button.state = False
            self.notify(button)
        if value != button.state and value == 1:
            button.state = True

    def check_rotary_encoder(self, rotary):
        rotary.update()
        if self.rotary.pos_prev != self.rotary.pos:
            if (self.rotary.pos / 4) % 1 == 0:
                self.notify(rotary)
            self.rotary.pos_prev = self.rotary.pos

    def process_events(self):
        self.check_button_press(self.rotary_button)
        self.check_button_press(self.button1)
        self.check_button_press(self.button2)
        self.check_button_press(self.button3)
        self.check_rotary_encoder(self.rotary)
