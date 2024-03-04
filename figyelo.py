import RPi.GPIO as GPIO
import cv2
import time

GPIO.setmode(GPIO.BCM) #GPIO.setmode(GPIO.BOARD)
trigPin=4              #trigPin=7
echoPin=17             #echoPin=11
GPIO.setup(trigPin,GPIO.OUT)
GPIO.setup(echoPin,GPIO.IN)


cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc('m', 'p','4', 'v')

frame_size = (int(cap.get(3)),int(cap.get(4)))

video=0
detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 20

while True:
    
    ret,frame = cap.read()
    
    GPIO.output(trigPin,0)
    time.sleep(2E-6)
    GPIO.output(trigPin,1)
    time.sleep(10E-6)
    GPIO.output(trigPin,0)
        
    while GPIO.input(echoPin)==0:
        pass
    echoStartTime=time.time()
        
    while GPIO.input(echoPin)==1:
        pass
    echoStopTime=time.time()
        
    pingTravelTime=echoStopTime-echoStartTime
    distance= int(((767*pingTravelTime*5280*12/3600)/2)*2.54)
     
    
    
    if distance<=10:
    
        if detection:
            timer_started = False
        else:
            detection = True
            video=video+1
            out = cv2.VideoWriter(f"video{video}.mp4",fourcc,8, frame_size)
            print("Started recording")
    elif detection:
        if timer_started:
            if time.time()- detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print('Stop recording')
        else:
                
            timer_started = True
            detection_stopped_time= time.time()
    if detection:
        out.write(frame)
    
    cv2.imshow("Camera",frame)
    
    if cv2.waitKey(1) == ord('q'):
        break
    
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()
