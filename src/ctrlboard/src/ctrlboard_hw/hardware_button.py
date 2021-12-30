class HardwareButton:
    state = True
    name = "n/a"
    pca_driver = None
    pin = 0

    def __init__(self, pca_driver, pin):
        self.pca_driver = pca_driver
        self.pin = pin

    def read(self):
        return self.pca_driver.read_port(self.pin)
