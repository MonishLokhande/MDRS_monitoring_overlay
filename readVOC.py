from machine import Pin as pin
import machine
import time

VOC_power = pin(0, pin.OUT)
VOC_power.value(1)
VOC_outputA = pin(20, pin.IN)

try:
    airQaulityList = [0] * 10
    idx = 0
    while True:
        # sensor output runs in 100ms  / 0.1 second cycle
        # low for 100ms means pollution class 0
        # low for 90 means pollution class 1
        # low for 0 means pollution class 10

        # tested with my roomates breath, detects alcohol
        # print("A: "+ str(VOCinputA.value()))

        if idx == 10:
            idx = 0
        airQaulityList[idx] = VOC_outputA.value()
        pollutionClass = airQaulityList.count(1)

        time.sleep(0.01) # 10 ms
        print(pollutionClass)
except KeyboardInterrupt:    
    VOC_power.value(0)
    print("Exited Successfully")