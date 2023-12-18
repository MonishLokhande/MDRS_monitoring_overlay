from machine import Pin as pin
import machine
import time

def record_data(file_name = 'dust_data.txt'):
    PM = machine.ADC(pin(26))
    import time
    
    # saving timestamp to file
    curr_time = time.localtime()
    time_stamp = str(str(curr_time[1])+'_'+ str(curr_time[2]) +'_'+ str(curr_time[0]) +'_' + str(curr_time[3]) +":"+ str(curr_time[4]))
    with open(file_name, 'a') as output_file:
        output_file.write("dust values saved at {}\n".format(time_stamp))
    
    # for x in range(10):
    PM_value = PM.read_u16()
    # equation from http://www.howmuchsnow.com/arduino/airquality/
    dustDensity = 0.17 * PM_value - 0.1
    # saving value
    with open(file_name, 'a') as output_file:
        output_file.write(str(dustDensity)+'\n')
    print(dustDensity)
        # time.sleep(0.5)
    

if __name__ == "__main__":
    try:
        while True:
            time.sleep(1)
            record_data()
    except KeyboardInterrupt:
        print("Exited Successfully")