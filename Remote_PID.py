'''
IOLine.DIO0_AD0 = (‘DIO0/AD0’, 0, ‘D0’)
IOLine.DIO1_AD1 = (‘DIO1/AD1’, 1, ‘D1’)
IOLine.DIO2_AD2 = (‘DIO2/AD2’, 2, ‘D2’)
IOLine.DIO3_AD3 = (‘DIO3/AD3’, 3, ‘D3’)
IOLine.DIO4_AD4 = (‘DIO4/AD4’, 4, ‘D4’)
IOLine.DIO5_AD5 = (‘DIO5/AD5’, 5, ‘D5’)
IOLine.DIO6 = (‘DIO6’, 6, ‘D6’)
IOLine.DIO7 = (‘DIO7’, 7, ‘D7’)
IOLine.DIO8 = (‘DIO8’, 8, ‘D8’)
IOLine.DIO9 = (‘DIO9’, 9, ‘D9’)
IOLine.DIO10_PWM0 = (‘DIO10/PWM0’, 10, ‘P0’, ‘M0’)
IOLine.DIO11_PWM1 = (‘DIO11/PWM1’, 11, ‘P1’, ‘M1’)
IOLine.DIO12 = (‘DIO12’, 12, ‘P2’)
IOLine.DIO13 = (‘DIO13’, 13, ‘P3’)
IOLine.DIO14 = (‘DIO14’, 14, ‘P4’)
IOLine.DIO15 = (‘DIO15’, 15, ‘P5’)
IOLine.DIO16 = (‘DIO16’, 16, ‘P6’)
IOLine.DIO17 = (‘DIO17’, 17, ‘P7’)
IOLine.DIO18 = (‘DIO18’, 18, ‘P8’)
IOLine.DIO19 = (‘DIO19’, 19, ‘P9’)
'''

'''
# Instantiate an XBee device object.
local_xbee = XBeeDevice("COM1", 9600)
local_xbee.open()

# Instantiate a remote XBee device object.
remote_xbee = RemoteXBeeDevice(local_xbee, XBee64BitAddress.from_hex_string("0013A20012345678"))

# Configure the DIO1_AD1 line of the local device to be Digital output (set high by default).
local_xbee.set_io_configuration(IOLine.DIO1_AD1, IOMode.DIGITAL_OUT_HIGH)

# Configure the DIO2_AD2 line of the local device to be Digital input.
local_xbee.set_io_configuration(IOLine.DIO2_AD2, IOMode.DIGITAL_IN)

# Configure the DIO3_AD3 line of the remote device to be Analog input (ADC).
remote_xbee.set_io_configuration(IOLine.DIO3_AD3, IOMode.ADC)

# Configure the DIO10_PWM0 line of the remote device to be PWM output (PWM).
remote_xbee.set_io_configuration(IOLine.DIO10_PWM0, IOMode.PWM)
'''

'''
# IO
set_dio_value(io_line, io_value)
# PWM
set_pwm_duty_cycle(io_line, cycle) cycle:0~100
'''

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
# Obtain the remote XBee device from the XBee network.
#xbee_network = local_device.get_network()
# リモートデバイス名を定義
#remote_device = xbee_network.discover_device(REMOTE_NODE_ID)

#remote_device = RemoteXBeeDevice(local_device, XBee64BitAddress.from_hex_string("0013A2004196AE62"))
remote_device = RemoteXBeeDevice(local_device, XBee64BitAddress.from_hex_string("0013A20041767079"))

def main():

    print(" +---------------------+")
    print(" | PWM Duty Cycle Test |")
    print(" +---------------------+\n")

    try:
        # ローカルデバイスと通信開始
        local_device.open()



        '''******************************************
        *************** 制御プログラム ***************
        ******************************************'''
        while True:
            # ピンモード設定 PWM
            remote_device.set_io_configuration(MOTOR_PWM, IOMode.PWM)
            #remote_device.set_io_configuration(MOTOR_1, IOMode.DIGITAL_OUT)
            #remote_device.set_io_configuration(MOTOR_2, IOMode.DIGITAL_OUT)
            remote_device.set_io_configuration(SENSOR_1, IOMode.ADC)
            remote_device.set_io_configuration(SENSOR_2, IOMode.ADC)

            # センサ値をGET
            #sensor_1 = remote_device.get_adc_value(SENSOR_1)
            #sensor_2 = remote_device.get_adc_value(SENSOR_2)

            #pwm_1 = sensor_1 / 4 #PWM 0~100%
            pwm_1 = 30

            if pwm_1 >= 100:
                pwm_1 = 100

            # 出力を設定
            remote_device.set_pwm_duty_cycle(MOTOR_PWM, pwm_1)
            remote_device.set_dio_value(MOTOR_1, IOMode.DIGITAL_OUT_HIGH) #CCW
            remote_device.set_dio_value(MOTOR_2, IOMode.DIGITAL_OUT_LOW)

            '''
            if sensor_1 >= sensor_2:
                remote_device.set_dio_value(MOTOR_1, IOMode.DIGITAL_OUT_HIGH) #CW
                remote_device.set_dio_value(MOTOR_2, IOMode.DIGITAL_OUT_LOW)
            else:
                remote_device.set_dio_value(MOTOR_1, IOMode.DIGITAL_OUT_LOW) #CCW
                remote_device.set_dio_value(MOTOR_2, IOMode.DIGITAL_OUT_HIGH)
            '''



            #PWM = remote_device.get_adc_value(IOLINE_IN)
            #test = remote_device.get_dio_value(MOTOR_1)

            #a = [sensor_1, sensor_2, pwm_1]
            #print(a)
            #print(sensor_1),
            #print(sensor_2),
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
