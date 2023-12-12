# Doesn't run on pico, just for example

GPIO.setup(26, GPIO.OUT)
GPIO.setup(13, GPIO.IN)
GPIO.setup(6, GPIO.OUT)

GPIO.output(6, GPIO.LOW)

timestamp = datetime.now().strftime('%b_%d_%Y-%H-%M')
pressLog = open("{}_button_log.txt".format(timestamp), 'w')

try:
    while(1):
        if GPIO.input(13):
            GPIO.output(6, GPIO.HIGH)
            pressLog.write(datetime.now().strftime('%b_%d-%H-%M-%S'+": ON\n"))
        else:
            GPIO.output(6, GPIO.LOW)
            pressLog.write(datetime.now().strftime('%b_%d-%H-%M-%S'+": OFF\n"))
        
        GPIO.output(26, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(26, GPIO.LOW)
        time.sleep(0.5)

except KeyboardInterrupt:
    pressLog.close()