

def setup_pins():
    from machine import Pin as pin
    from time import sleep
    
    CO2_power = pin(15, pin.OUT)
    CO2_power.value(1)

    pwm_reading = pin(12, pin.IN)
    sleep(0.5) # allow temp sensor time to reach idle state
    
    return CO2_power, pwm_reading

def record_data(sensor_pin, file_name = "CO2_data.txt"):

    import time


    curr_time = time.localtime()
    time_stamp = str(str(curr_time[1])+'_'+ str(curr_time[2]) +'_'+ str(curr_time[0]) +'_' + str(curr_time[3]) +":"+ str(curr_time[4]))
    with open(file_name, 'a') as output_file:
        output_file.write("CO2 values saved at {}\n".format(time_stamp))
    cycle_list = [0] * 1000
    for check_idx in range(1000):
        time.sleep(0.0009) # just less than every ms to account for timing offsets
        cycle_list[check_idx] = sensor_pin.value()
    CO2_reading = str(2000 * cycle_list.count(1)/1000)
    with open(file_name, 'a') as output_file:
        output_file.write(CO2_reading)
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
    
    try:
        while True:
            time.sleep(1) # every second
            record_data(sensor_reading_pin, fileName)
    
                
    except KeyboardInterrupt:
        CO2_power_pin.value(0)
        print("Exited Successfully")