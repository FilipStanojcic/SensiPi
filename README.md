# Description
Program integrates multiple sensor-driven components with a Raspberry Pi, allowing real-time input processing and actuator control. 

By leveraging an ultrasonic distance sensor, photoresistor-based AD/DA conversion, a servo motor, and an LED, the system dynamically adjusts brightness and movement based on environmental readings.

Users can toggle between two inputs sources: distance measurement and light intensity. Changes are reflected in hardware behaviour.

![image](https://github.com/user-attachments/assets/939225b7-0453-4e5d-91a2-0e9e0971d3a1)

![Filip S  Integration Block Diagram](https://github.com/user-attachments/assets/dd61ddfa-1871-4944-a325-ae0a7f650aea)

Upon program execution, the Ultrasonic Sensor will:
  - Take reading from environment, maximum of 4m, minimum on 0.02m.
  - Output reading to command line, if limit is exceeded, "invalid distance".
  - Reading is taken by LED, dimming in brightness the lower the reading.
  - Reading is taken by Motor, arm angles from 0°-180°, 0° = 0.02m up to 180° = 4m

User has the option to toggle input environemnt to Photoresistor on AD/DA module.

Upon User typing 't' and pressing 'enter' input switches to Photoresistor that will:
  - Take reading from environemnt, maximum of 3.3V, minimum of 0V (255-0 digitally).
  - Output reading to command line.
  - Reading is taken by LED, dimming in brightness.
  - Reading is taken by Motor, arm angles from 0°-180°, 0° = 3.3V up to 180° = 0V.

User may toggle back to Distance Sensor with 't' -> 'enter' input combination.

User may interrupt and press 'enter' to exit program.

Upon exiting program:
  - Servo Motor returns to neutral position, ~90°.
  - Led stops PWM and maintains default brightness.

# Execution/Functionality
Download integration.py to your device. Ensure the file is placed on your Raspberry Pi, whether through mounting, online copying, or any method.

In a command terminal (Windows CMD, Powershell, Terminal, etc.) navigate to downloads using the "cd" command (for example: C:\User\fstan> cd Downloads) or wherever the files have been saved.

Run the program using "python integration.py".

Your device should be communicating with a Raspberry Pi over a TTL-serial cable. For the sake of this project, wire an LED, an Ultrasonic Ranging Module (HC - SR04), a 9g Micro Servo Motor (MG90), and an 8-bit A/D and D/A converter (PCF8591).

LED is connected with 220-ohm resistor, 3.3V and GROUND, and wire to GPIO 13.

Ultrasonic Distance Sensor TRIGGER and ECHO are wired to GPIO 18 and 17 respectively, with 3.3V and GROUND.

AD/DA Converter Module is connected with 3.3V and GROUND, with SCL and SDA wired to respective pins on the Raspberry Pi Breakout Cobbler.

Servo Motor is connected with 5V and GROUND, and wire to GPIO 12.

Cobbler is wired to laptop for operator input and output.

GPIO pins are set to Broadcom, pin numbers are identified, I/O is set.

Converter Module A0 is set to 0x40 for photoresistor mounted on device to be used.

Servo Motor is set to 50Hz frequency (period of 20 ms) with PWM.

LED is set to 1000Hz frequency with PWM.

These devices can be wired in many ways, so if need be, edit integration.py however necessary to match wiring to the defined GPIO pins, no other changes should be needed.

# Difficulties

