

def setup_pins():
    from machine import Pin as pin
    from time import sleep
    
    CO2_power = pin(15, pin.OUT)
    CO2_power.value(1)

    pwm_reading = pin(12, pin.IN, pin.PULL_UP)
    sleep(0.5) # allow temp sensor time to reach idle state
    
    return pwm_reading, CO2_power

def read_analog():
    from machine import ADC
    from machine import Pin as pin
    CO2 = ADC(pin(28, pin.IN))
    CO2_value = CO2.read_u16()
    return CO2_value
    
def get_value(sensor_pin):
    from time import sleep
    cycle_list = [0] * 1000
    for check_idx in range(1000):
        sleep(0.0009) # just less than every ms to account for timing offsets
        cycle_list[check_idx] = sensor_pin.value()
        # print('sensor_pin: ' + str(sensor_pin.value()))
    CO2_reading = str(2000 * cycle_list.count(1)/1000)

    return CO2_reading

def record_data(sensor_pin, file_name = "CO2_data.csv"):

    import time


    curr_time = time.localtime()
    time_stamp = str(str(curr_time[1])+'_'+ str(curr_time[2]) +'_'+ str(curr_time[0]) +'_' + str(curr_time[3]) +":"+ str(curr_time[4]))
    
    with open(file_name, 'a') as output_file:
        output_file.write(time_stamp+', ')
    cycle_list = [0] * 1000
    
    # for check_idx in range(1000):
        # time.sleep(0.0009) # just less than every ms to account for timing offsets
        # cycle_list[check_idx] = sensor_pin.value()
        # print('sensor_pin: ' + str(sensor_pin.value()))
    # CO2_reading = str(2000 * cycle_list.count(1)/1000)
    CO2_reading = str(read_analog())
    
    with open(file_name, 'a') as output_file:
        output_file.write(CO2_reading+',\n')
    print(CO2_reading)
    # for log in range(10):
    #     cycle_list = [0] * 1000
    #     for check_idx in range(1000):
    #         time.sleep(0.0009) # just less than every ms to account for timing offsets
    #         cycle_list[check_idx] = sensor_pin.value()
            
    #     # formula taken from sensor docs
    #     CO2_reading = str(2000 * cycle_list.count(1)/1000)
    #     with open(file_name, 'a') as output_file:
    #         output_file.write(CO2_reading)
    #     print(CO2_reading)
    #     time.sleep(0.5)

if __name__ == "__main__":
    
    from machine import Pin as pin
    import machine
    import time
    
    sensor_reading_pin, CO2_power_pin = setup_pins()
    curr_time = time.localtime()
    time_stamp = str(str(curr_time[1])+'_'+ str(curr_time[2]) +'_'+ str(curr_time[0]) +'_' + str(curr_time[3]) +":"+ str(curr_time[4]))
    fileName = "{}_{}.txt".format(time_stamp, "CO2_data")
    
    print("Saving results to {}".format(fileName))
    print("Timestamps are formatted Month_Day_Year_HH:MM")
    print('Power (should always be 1: )' + str(CO2_power_pin.value()))
    
    try:
        while True:
            time.sleep(1) # every second
            # record_data(sensor_reading_pin, fileName)
            print(read_analog())
            
    
                
    except KeyboardInterrupt:
        CO2_power_pin.value(0)
        print("Exited Successfully")

