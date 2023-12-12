from machine import Pin as pin
import machine
import time


adc = machine.ADC(4)

try:
    while True:
        time.sleep(1)
        adc_voltage = adc.read_u16() * (3.3 / (65536))
        temp_c = 27 - (adc_voltage - 0.706)/0.001721
        temp_f = 32+(1.8*temp_c)

        print(temp_f)
except KeyboardInterrupt:   
    print("Exited Successfully")