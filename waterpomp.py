import notifications

import RPi.GPIO as GPIO
from time import sleep


def start():
    GPIO.setmode(GPIO.BCM)

    INPUT_PIN = 17
    POWER_PIN = 18

    GPIO.setup(INPUT_PIN, GPIO.IN)
    GPIO.setup(POWER_PIN, GPIO.OUT)

    GPIO.output(18, GPIO.LOW)

    water_detected = False
    while True:
        # Run every 1 second
        if water_detected:
            water_detected = False
            notifications.push_webhook_cardv2(waterpomp_started=False)
            GPIO.output(18, GPIO.LOW)
            sleep(86400)  # 24u

        sleep(1)
        result = GPIO.input(INPUT_PIN)
        print(f'running: {result}')

        # If water is detected result is 0
        if result == 0:
            notifications.push_webhook_cardv2(waterpomp_started=True)
            GPIO.output(18, GPIO.HIGH)
            sleep(300)  # 5 min
            water_detected = True
        else:
            GPIO.output(18, GPIO.LOW)


start()
