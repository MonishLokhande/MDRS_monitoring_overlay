from machine import Pin as pin
import machine
import time

def record_data(file_name = "temp_data.txt"):

    import time

    adc = machine.ADC(4)
    curr_time = time.localtime()
    time_stamp = str(str(curr_time[1])+'_'+ str(curr_time[2]) +'_'+ str(curr_time[0]) +'_' + str(curr_time[3]) +":"+ str(curr_time[4]))
    with open(file_name, 'a') as output_file:
        output_file.write("temp values saved at {}\n".format(time_stamp))
    
    # for x in range(10):
    adc_voltage = adc.read_u16() * (3.3 / (65536))
    temp_c = 27 - (adc_voltage - 0.706)/0.001721
    temp_f = 32+(1.8*temp_c)

    # saving value
    with open(file_name, 'a') as output_file:
        output_file.write(str(temp_f)+'\n')
    print(temp_f)
    # time.sleep(0.5)

if __name__ == "__main__":
    try:
        while True:
            time.sleep(1)
            
            print("Recording temp data")
            record_data()

    except KeyboardInterrupt:   
        print("Exited Successfully")