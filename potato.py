import time
import RPi.GPIO as GPIO
import threading

GPIO_LIST = {
    'switch':  13,
    'led_red': 19,
    'speaker': 26
}

alam_flag = False

def sound_alam():
    merody = [1567.982, 1396.913, 1567.982, 0.0001]
    p = GPIO.PWM(GPIO_LIST['speaker'], 1)
    
    while alam_flag:
        for i, hz in enumerate(merody):
            p.start(50)
            p.ChangeFrequency(hz)
            if i % 2 == 0:
                GPIO.output(GPIO_LIST['led_red'], GPIO.HIGH)
            else:
                GPIO.output(GPIO_LIST['led_red'], GPIO.LOW)
            
            time.sleep(0.3)
            p.stop()
            if not(alam_flag): break
    
    GPIO.output(GPIO_LIST['led_red'], GPIO.LOW)

    
def main():
    global alam_flag

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_LIST['led_red'], GPIO.OUT)
    GPIO.setup(GPIO_LIST['switch'], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(GPIO_LIST['speaker'], GPIO.OUT, initial=GPIO.LOW)
    task = None

    try:
        while True:
            if GPIO.input(GPIO_LIST['switch']) == False:
                if alam_flag:
                    alam_flag = False
                    task.join()
                    task = None
                    print('stopped!')
                else:
                    alam_flag = True
                    task = threading.Thread(target=sound_alam)
                    task.start()
                    print('alam started!')
            time.sleep(0.2 )
            
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        print('exit')

if __name__ == '__main__':
    main()
