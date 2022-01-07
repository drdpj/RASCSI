from ctrlboard_hw.hardware_button import HardwareButton


class Encoder:
    def __init__(self, enc_a: HardwareButton, enc_b: HardwareButton):
        self.enc_a = enc_a
        self.enc_b = enc_b
        self.pos = 0
        self.scaled_pos = 0
        self.direction = 0

    def update(self):
        if self.enc_a.state_interrupt is True and self.enc_b.state_interrupt is True:
            return

        if self.enc_a.state_interrupt is False and self.enc_b.state_interrupt is False:
            self.enc_a.state_interrupt = True
            self.enc_b.state_interrupt = True
            return

        self.direction = 0

        if self.enc_a.state_interrupt is False:
            self.pos += 1
            self.direction = 1
        elif self.enc_a.state_interrupt is True:
            self.pos -= 1
            self.direction = -1

        self.scaled_pos = int(self.pos)

        self.enc_a.state_interrupt = True
        self.enc_b.state_interrupt = True

