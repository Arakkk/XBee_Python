from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
import time
import threading

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM3"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

REMOTE_NODE_ID = "REMOTE"

# ピン名定義
MOTOR_1 = IOLine.DIO12
MOTOR_2 = IOLine.DIO4_AD4

def main():

    print(" +---------------------+")
    print(" | PWM Duty Cycle Test |")
    print(" +---------------------+\n")

    local_device = XBeeDevice(PORT, BAUD_RATE)

    try:
        # Obtain the remote XBee device from the XBee network.
        xbee_network = local_device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)

        local_device.open()
        # ピンモード設定 PWM
        local_device.set_io_configuration(IOLine.DIO11_PWM1, IOMode.PWM)
        remote_device.set_io_configuration(MOTOR_1, IOMode.DIGITAL_OUT)
        remote_device.set_io_configuration(MOTOR_2, IOMode.DIGITAL_OUT)


        # PWMを設定
        local_device.set_pwm_duty_cycle(IOLine.DIO11_PWM1, 200)
        remote_device.set_dio_value(MOTOR_1, HIGH)
        remote_device.set_dio_value(MOTOR_2, LOW)

        #
        dc2 = local_device.get_pwm_duty_cycle(IOLine.DIO11_PWM1)


        assert (dc2 == 100)

        print("Test finished successfully")

    # 通信終了
    finally:
        if local_device is not None and local_device.is_open():
            local_device.close()


if __name__ == "__main__":
    main()
