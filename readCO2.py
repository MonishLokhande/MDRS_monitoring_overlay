from machine import Pin as pin
import machine
import time

CO2_power = pin(15, pin.OUT)
CO2_power.value(1)

pwm_reading = pin(12, pin.IN)
time.sleep(0.5) # allow temp sensor time to reach idle state

curr_time = time.localtime()
file_stamp = str(str(curr_time[1])+'_'+ str(curr_time[2]) +'_'+ str(curr_time[0]) +'_' + str(curr_time[3]) +":"+ str(curr_time[4]))
output_file = open("{}_pwm_output.txt".format(file_stamp), 'w')
print("Outputting results {}_pwm_output.txt".format()file_stamp)
print("Timestamps are Month, Day, Year-Time")

try:
    while True:
        time.sleep(60) # every minute
        # getting current time, converting to strings, then writing to file
        curr_time = time.localtime()
        timestamp = str(str(curr_time[1])+', '+ str(curr_time[2]) +', '+ str(curr_time[0]) +'-' + str(curr_time[3]) +":"+ str(curr_time[4]))
        output_file.write('Timestamped {}:\n'.format(timestamp))
        print('Timestamp {} Started'.format(timestamp))

        for second in range(10): # checks in 20 second, 10 value clusters clusters
            time.sleep(1) # with 1 second intervals
            # total cycle 1004ms long, min of 2ms on and 2 ms off
            # checks 1000 times per second / cycle
            cycle_list = [0] * 1000
            for check_idx in range(1000):
                time.sleep(0.0009) # just less than every ms to account for timing offsets
                cycle_list[check_idx] = pwm_reading.value()
            # formula taken from sensor docs
            output_file.write(str(2000 * cycle_list.count(1)/1000) + '\n')
except KeyboardInterrupt:
    CO2_power.value(0)
    output_file.close()
    print("Exited Successfully")