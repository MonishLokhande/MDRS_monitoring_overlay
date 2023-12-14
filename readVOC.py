from machine import Pin as pin
import machine
import time

def setup_pins():
    from machine import Pin as pin
    VOC_power = pin(21, pin.OUT)
    VOC_power.value(1)

    VOC_outputA = pin(20, pin.IN)
    return VOC_power, VOC_outputA

def record_data(input_pin, file_name = 'VOC_data.txt'):
    # sensor output runs in 100ms  / 0.1 second cycle
    # low for 100ms means pollution class 0
    # low for 90 means pollution class 1
    # low for 0 means pollution class 10
    from time import sleep
    
    VOC_value_list = [0] * 10
    idx = 0
    
    # initial timestamp
    curr_time = time.localtime()
    time_stamp = str(str(curr_time[1])+'_'+ str(curr_time[2]) +'_'+ str(curr_time[0]) +'_' + str(curr_time[3]) +":"+ str(curr_time[4]))
    with open(file_name, 'a') as output_file:
        output_file.write("10 VOC values saved at {}\n".format(time_stamp))
    

    for x in range(10):
        for y in range(11): # 10 values make 1 new reading, extra for averaging across many bad timings
            if idx == 10:
                idx = 0
            VOC_value_list[idx] = input_pin.value()
            pollutionClass = VOC_value_list.count(1)
            idx += 1
            sleep(0.01) # 10 ms
        
        # saving value
        with open(file_name, 'a') as output_file:
            output_file.write(str(pollutionClass)+'\n')
        print(pollutionClass)
        sleep(0.5)


if __name__ == "__main__":
    power_pin, data_pin = setup_pins()
    try:
        while True:
        
            time.sleep(1)
            record_data(data_pin)
    except KeyboardInterrupt:    
        power_pin.value(0)
        print("Exited Successfully")