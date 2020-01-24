
from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress
from digi.xbee.io import IOLine, IOMode
import time
import threading

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM4"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

REMOTE_NODE_ID = "REMOTE"

# ピン名定義
MOTOR_1 = IOLine.DIO12
MOTOR_2 = IOLine.DIO4_AD4
MOTOR_PWM = IOLine.DIO11_PWM1
SENSOR_1 = IOLine.DIO1_AD1
SENSOR_2 = IOLine.DIO2_AD2

# ローカルデバイス名を定義
local_device = XBeeDevice(PORT, BAUD_RATE)
# リモートデバイス名を定義
remote_device = RemoteXBeeDevice(local_device, XBee64BitAddress.from_hex_string("0013A20041767079"))

def main():

    print(" +---------------------+")
    print(" | PWM Duty Cycle Test |")
    print(" +---------------------+\n")

    try:
        # ローカルデバイスと通信開始
        local_device.open()

        # ピンモード設定 PWM
        remote_device.set_io_configuration(MOTOR_PWM, IOMode.PWM)
        #remote_device.set_io_configuration(MOTOR_1, IOMode.DIGITAL_OUT)
        #remote_device.set_io_configuration(MOTOR_2, IOMode.DIGITAL_OUT)
        remote_device.set_io_configuration(SENSOR_1, IOMode.ADC)
        remote_device.set_io_configuration(SENSOR_2, IOMode.ADC)

        '''******************************************
        *************** 制御プログラム ***************
        ******************************************'''
        while True:
            pwm_1 = 30

            # 出力を設定
            remote_device.set_pwm_duty_cycle(MOTOR_PWM, pwm_1)
            remote_device.set_dio_value(MOTOR_1, IOMode.DIGITAL_OUT_HIGH) #CCW
            remote_device.set_dio_value(MOTOR_2, IOMode.DIGITAL_OUT_LOW)

            print(pwm_1)

        '''******************************************
        *************** 制御プログラム END ***********
        ******************************************'''

    # 通信終了
    finally:
        if local_device is not None and local_device.is_open():
            local_device.close()


if __name__ == "__main__":
    main()
