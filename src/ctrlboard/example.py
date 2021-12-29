"""
Pca 9554 basic usage example
"""
import time

import pca9554

# mapping:
# io0/pin4=rotary enc a
# io1/pin5=rotary enc b
# io2/pin6=button 1
# io3/pin7=button 2
# io4/pin9=button 3
# io5/pin10=button 4/rotary button
# io6/pin11=led 1
# io7/pin12=led 2


def example():
    # init
    i2c_address = 0x3f
    pca_driver = pca9554.Pca9554(i2c_address)

    # enable pins 0 and 1 to be inputs
    pca_driver.write_config_port(0, pca9554.INPUT)
    pca_driver.write_config_port(1, pca9554.INPUT)
    pca_driver.write_config_port(2, pca9554.INPUT)
    pca_driver.write_config_port(3, pca9554.INPUT)
    pca_driver.write_config_port(4, pca9554.INPUT)
    pca_driver.write_config_port(5, pca9554.INPUT)
    pca_driver.write_config_port(6, pca9554.OUTPUT)
    pca_driver.write_config_port(7, pca9554.OUTPUT)

#    # enable all others to be outputs
#    for i in range(2, 8):
#        pca_driver.write_config_port(i, pca9554.OUTPUT)

    # supposedly, a sensor is connected to input 0 or 1 (or both), so values can be read from it

    # read values in a loop
    while True:
        rotary_a = pca_driver.read_port(0)
        rotary_b = pca_driver.read_port(1)

        button1 = pca_driver.read_port(2)
        button2 = pca_driver.read_port(3)
        button3 = pca_driver.read_port(4)
        button_rotary = pca_driver.read_port(5)

        print("button1: " + str(button1))
        print("button2: " + str(button2))
        print("button3: " + str(button3))
        print("button rotary: " + str(button_rotary))
        print("rotary a: " + str(rotary_a))
        print("rotary b: " + str(rotary_b))

        # wait a bit
        time.sleep(0.05)


if __name__ == '__main__':
    example()
