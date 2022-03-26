import time

from numpy import take
from DistanceEstimation import *
import cv2 as cv
from pyax12.connection import Connection
import datetime


detect_1= detect()

#Connect to the serial port
serial_connection = Connection(port="COM3", baudrate=1000000)
# create AX12 instance with ID
motor_id1 = 1
motor_id2 = 2
motor_id3 = 3
motor_id4 = 4
motor_id5 = 5
motor_id6 = 6

def jarak_gripper():
    jarak =2
    return jarak

#Parking arm robot
def arm_neutral():
    serial_connection.goto(motor_id1, 90, speed=250, degrees=True)
    time.sleep(1)
    serial_connection.goto(motor_id2, 60, speed=250, degrees=True)
    serial_connection.goto(motor_id3, -60, speed=250, degrees=True)
    time.sleep(1)
    serial_connection.goto(motor_id4, 20, speed=250, degrees=True)
    time.sleep(1)
    serial_connection.goto(motor_id5, 20, speed=250, degrees=True)
    time.sleep(1)

def buka():
    serial_connection.goto(motor_id6, 40, speed=150, degrees=True)
    time.sleep(1)
    #kurang lebih 2 inch
def tutup():
    serial_connection.goto(motor_id2, -40, speed=150, degrees=True)
    time.sleep(1)

def pick():
    arm_neutral()
    if detect_1.distance_finder <= jarak_gripper():
        buka()
        time.sleep(1)
        tutup()
        time.sleep(1)

def place():
    arm_neutral()
    if detect_1.distance_finder <= jarak_gripper():
        tutup()
        time.sleep(1)
        buka()
        time.sleep(1)

###
def Jarak_prioritas(jarak1):
    if jarak1 >= 0 & jarak1 <=2:
        print("Prioritas 1: ")
    elif jarak1 >= 3 & jarak1 <= 5 :
        print('Prioritas 2:')
    elif jarak1 >= 6 & jarak1 <= 8 :
        print('Prioritas 3:')
    elif jarak1 >= 9 & jarak1 <= 11 :
        print('Prioritas 4:')
    elif jarak1 >= 12 & jarak1 <= 14 :
        print('Prioritas 5:')

def Jarak():
    if  Jarak_prioritas in detect_1.distance_finder  == True:
        pick()
        time.sleep(1)
        place()
        time.sleep(1)
## TANDA TANYA ?

def matang(): # jika matang akan ditaruh box matang
    # MOtor 2 dan 3
    #Jarak()
    serial_connection.goto(motor_id1, 0, speed=150, degrees=True)
    time.sleep(1)
    serial_connection.goto(motor_id2, -20, speed=150, degrees=True)
    serial_connection.goto(motor_id3, 20, speed=150, degrees=True)
    time.sleep(1)
    serial_connection.goto(motor_id4, 20, speed=150, degrees=True)
    time.sleep(1)
    serial_connection.goto(motor_id5, 20, speed=150, degrees=True)
    time.sleep(1)

def busuk(): # jika busuk akan ditaruh box busuk
    # MOtor 2 dan 3
    #Jarak()
    serial_connection.goto(motor_id1, 90, speed=250, degrees=True)
    time.sleep(1)
    serial_connection.goto(motor_id2, -20, speed=250, degrees=True)
    serial_connection.goto(motor_id3, 20, speed=250, degrees=True)
    time.sleep(1)
    serial_connection.goto(motor_id4, 20, speed=250, degrees=True)
    time.sleep(1)
    serial_connection.goto(motor_id5, 20, speed=250, degrees=True)
    time.sleep(1)

    

ref_matang = cv.imread(r'E:\tutu\ReferenceImages\image6.png')
ref_mentah = cv.imread(r'E:\tutu\ReferenceImages\image10.png')
ref_busuk  = cv.imread(r'E:\tutu\ReferenceImages\image3.png')

mentah_data = detect_1.object_detector(ref_mentah)
mentah_width_in_rf = mentah_data[0][1]

matang_data = detect_1.object_detector(ref_matang)
matang_width_in_rf = matang_data[0][1]

busuk_data = detect_1.object_detector(ref_busuk)
busuk_width_in_rf = busuk_data[0][1]

# reading the reference image from dir 
print(f"matang width in pixels : {matang_width_in_rf} mentah width in pixel: {mentah_width_in_rf} busuk width in pixel: {busuk_width_in_rf}")

# finding focal length 
focal_person = detect_1.focal_length_finder(KNOWN_DISTANCE, MATANG_WIDTH, matang_width_in_rf)

focal_mobile = detect_1.focal_length_finder(KNOWN_DISTANCE, MENTAH_WIDTH, mentah_width_in_rf)

focal_busuk = detect_1.focal_length_finder(KNOWN_DISTANCE, BUSUK_WIDTH, busuk_width_in_rf)

# jarak prioritas

#FPS
fps_start_time = datetime.datetime.now()
fps = 0
total_frames = 0
Jumlah_matang = 0
Jumlah_busuk = 0
# fine tuning mencari hasil weiht terbaik ( biasane last weight)

# arm_neutral()
# def take_foto():
    
#     global ret,takee
#     ret,takee = cap.read()
#     time.sleep(2)
#     cv.imwrite(r'E:\RobotArm\foto')
#     cap.release()
#     image = cv.imread('/home/pi/Desktop/img/image3.jpg') # Load image for analysis.
#     gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) # Convert image to grayscale.
#     edged = cv.Canny(gray, 25, 100) # Apply edge detector with threshold (converts to B&W).
#     edged = cv.dilate(edged, (5,5), iterations=5) # Pixel expansion.
    
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    data = detect_1.object_detector(frame)

    #FPS :v
    total_frames = total_frames + 1
    fps_end_time = datetime.datetime.now()
    time_diff = fps_end_time - fps_start_time
    if time_diff.seconds == 0:
        fps = 0.0
    else:
        fps = (total_frames / time_diff.seconds)

        fps_text = "FPS: {:.2f}".format(fps)
    #FPS :v
    
    # counter buah
    Total = [d[0] for d in data]
    if len(Total) > 0 :   
        Jumlah_matang= ("Matang: ",Total.count('matang')) 
        Jumlah_busuk =("Busuk: ",Total.count('busuk')) 
    # counter buah

    for d in data:
        if d[0] =='matang':
            distance = detect_1.distance_finder(focal_person, MATANG_WIDTH, d[1])
            x, y = d[2]
            matang()
            time.sleep(0.5)
            arm_neutral()
            
        elif d[0] =='mentah':
            distance = detect_1.distance_finder (focal_mobile, MENTAH_WIDTH, d[1])
            x, y = d[2]
        elif d[0] =='busuk':
            distance = detect_1.distance_finder (focal_busuk, BUSUK_WIDTH, d[1])
            x, y = d[2]
            busuk()
            time.sleep(0.5)
            arm_neutral()



        cv.circle(frame,(int(d[3]),int(d[4])),4,(0,255,0),-1)
        xbaru = int(d[3]) - int(int(d[5])/2)
        ybaru = int(d[4])
        # theta = math.atan2(xbaru,int(d[4]))
        

        # print(math.degrees (theta))
        # print(distance)
        # xreal= distance*math.cos (theta)
        # yreal= distance*math.sin (theta)
        # print("box 0",d[0])
        # print("Koordinat x= ",xreal)
        # print("Koordinat y= ",yreal)
        
        print("Koordinat x dan y:", xbaru,ybaru)
        cv.rectangle(frame, (x, y-3), (x+150, y+23),BLACK,-1 )
        cv.putText(frame, f'Dis: {round(distance,2)} inch', (x+5,y+13), FONTS, 0.48, GREEN, 2)

    cv.putText(frame, fps_text, (5, 30), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, GREEN, 1)
    cv.putText(frame, str(Jumlah_matang),(5, 70), cv.FONT_HERSHEY_COMPLEX_SMALL, 1,RED, 1)
    cv.putText(frame, str(Jumlah_busuk), (5, 100), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, BLUE, 1)


    cv.imshow('frame',frame)
    
    key = cv.waitKey(2)
    if key ==ord('q'):
        break
cv.destroyAllWindows()
cap.release()