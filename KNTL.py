from pyax12.connection import Connection
from pyax12.argparse_default import common_argument_parser

from time import sleep


    # Connect to the serial port
serial_connection = Connection(port="COM3", baudrate=1000000)

    ###

motor_id1 = 1
motor_id2 = 2
motor_id3 = 3
motor_id4 = 4
motor_id5 = 5
motor_id6 = 6
        
while True:
    #GERAKKAN 1 netral
    serial_connection.goto(motor_id1, 90, speed=150, degrees=True)
    sleep(1)
    serial_connection.goto(motor_id2, 60, speed=150, degrees=True)
    serial_connection.goto(motor_id3, -60, speed=150, degrees=True)
    sleep(1)
    serial_connection.goto(motor_id4, 20, speed=150, degrees=True)
    sleep(1)
    serial_connection.goto(motor_id5, 20, speed=150, degrees=True)
    sleep(1)
# serial_connection.goto(motor_id6, 50, speed=150, degrees=True)
# sleep(1)
    #GERAKKAN 2
    serial_connection.goto(motor_id1, 0, speed=150, degrees=True)
    sleep(1)
    serial_connection.goto(motor_id2, -20, speed=150, degrees=True)
    serial_connection.goto(motor_id3, 20, speed=150, degrees=True)
    sleep(1)
    serial_connection.goto(motor_id4, -20, speed=150, degrees=True)
    sleep(1)
    serial_connection.goto(motor_id5, -20, speed=150, degrees=True)
    sleep(1)
    # serial_connection.goto(motor_id6, -50, speed=250, degrees=True)
    # sleep(1)
   

