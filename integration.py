import RPi.GPIO as GPIO
import time
import datetime
import smbus
import threading

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
TRIGGER_PIN = 18
ECHO_PIN = 17
SERVO_PIN = 12
LED_PIN = 13

GPIO.setup(TRIGGER_PIN,GPIO.OUT)
GPIO.setup(ECHO_PIN,GPIO.IN)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

# Constant variables in use
HIGH_TIME = 0.00001 # Pulse width
LOW_TIME = 1 - HIGH_TIME # Remaining loop time
SPEED_OF_SOUND = 330 / float(1000000)
MIN_DISTANCE = 0.02 # Meters
MAX_DISTANCE = 4.0 # Meters
MAX_VOLTAGE = 3.3 # Volts

# I2C setup
address = 0x48
A0 = 0x40 #photoresistor
bus = smbus.SMBus(1)

# Servo setup
servo = GPIO.PWM(SERVO_PIN, 50) # 50Hz frequency, period of 20 milliseconds
servo.start(50)
time.sleep(1)

# LED setup
led_pwm = GPIO.PWM(LED_PIN, 1000) # 1000Hz frequency
led_pwm.start(0)

def angle_to_duty_cycle(angle):
	MIN_DUTY_CYCLE = 2.5
	MAX_DUTY_CYCLE = 12.5
        return MIN_DUTY_CYCLE + (angle / 180) * (MAX_DUTY_CYCLE - MIN_DUTY_CYCLE)

def get_distance():
        GPIO.output(TRIGGER_PIN,GPIO.HIGH)
        # print 'Trigger HIGH'
        time.sleep(HIGH_TIME)
        GPIO.output(TRIGGER_PIN,GPIO.LOW)
        # print 'Trigger LOW'

        while GPIO.input(ECHO_PIN)==False:
        # pulse is LOW
                pass
        starttime = datetime.datetime.now().microsecond

        while GPIO.input(ECHO_PIN)==True:
        # pulse is HIGH
                pass

        # pulse is LOW
        endtime = datetime.datetime.now().microsecond
        travel_time = endtime - starttime
        distance = SPEED_OF_SOUND * travel_time / float(2)
        return distance

def read_photoresistor():
        bus.write_byte(address, A0)
        value = bus.read_byte(address)
        return value * MAX_VOLTAGE / 255 # Convert digital value to voltage level

stop_threads = False
use_distance_sensor = True

def toggle_sensor_mode():
        global stop_threads, use_distance_sensor
        while not stop_threads:
                input_key = input("Press 't' to toggle sensor mode: ").strip().lower()
                if input_key == 't':
                        use_distance_sensor = not use_distance_sensor
                        mode = "Distance Sensor" if use_distance_sensor else "Photoresistor"
                        print(f"Switched to {mode} mode.")

def handle_distance_sensor():
        distance = get_distance()
        if MIN_DISTANCE <= distance <= MAX_DISTANCE:
                print(f"Distance: {distance} meters")
                angle = (1 - (distance / MAX_DISTANCE)) * 180
                duty_cycle = angle_to_duty_cycle(angle)
                servo.ChangeDutyCycle(duty_cycle)

                brightness = (distance / MAX_DISTANCE) * 100

                brightness = max(0.0, min(100.0, brightness))
                led_pwm.ChangeDutyCycle(brightness)
        else:
                print("Invalid distance")
                led_pwm.ChangeDutyCycle(0)

def handle_photoresistor():
        photoresistor_value = read_photoresistor()
        print(f"Photoresistor: {photoresistor_value:.2f} V")

        brightness = max(0.0, min(100.0, (photoresistor_value / MAX_VOLTAGE) * 100))

        angle = (photoresistor_value / MAX_VOLTAGE) * 180
        duty_cycle = angle_to_duty_cycle(angle)
        servo.ChangeDutyCycle(duty_cycle)
        led_pwm.ChangeDutyCycle(brightness)

def control_loop():
        try:
                while not stop_threads:
                        if use_distance_sensor:
                                handle_distance_sensor()
                        else:
                                handle_photoresistor()
                        time.sleep(LOW_TIME)
        except KeyboardInterrupt:
                pass

control_thread = threading.Thread(target=control_loop)
input_thread = threading.Thread(target=toggle_sensor_mode)

control_thread.start()
input_thread.start()

try:
        while True:
                time.sleep(LOW_TIME)

except KeyboardInterrupt:
        print("Interrupt received. Stopping threads.")
        print("Press 'enter' key to quit.")
        stop_threads = True
        control_thread.join()
        input_thread.join()
        print("Exiting program.")

finally:
        servo.ChangeDutyCycle(7.5)
        time.sleep(1)
        servo.stop()
        led_pwm.stop()
        GPIO.cleanup()
