import machine
import time
try:
    import readCO2
    import readOnboardTemp
    import readPM2_5
    import readVOC
except:
    raise ValueError("Error importing files\nMake sure everything being imported is copied onto the pi and named exactly the same as specified in this file")  
    


def file_names_setup(suffix = '_log.csv'):
    file_names = {'CO2': 'CO2'+suffix,
                  'VOC':'VOC'+suffix,
                  'Temp':'Temp'+suffix,
                  'PM2.5':'PM2.5'+suffix}
    return file_names

def record_values(file_names):
    
    global CO2_reading_pin
    global VOC_reading_pin
    
    print("Recording CO2 values")
    # readCO2.record_data(CO2_reading_pin, file_names['CO2'])
    print(readCO2.read_analog())
    
    print("Recording VOC values")
    readVOC.record_data(VOC_reading_pin, file_names['VOC'])
    
    print("Recording temp values")
    readOnboardTemp.record_data(file_names['Temp'])
    
    print("Recording dust values")
    readPM2_5.record_data(file_names['PM2.5'])
    
debounce_time = 0

file_names = file_names_setup()
LED_pin = machine.Pin(7, machine.Pin.OUT)

def manual_data_read(pin):
    global debounce_time
    global LED_pin
    if (time.ticks_ms() - debounce_time > 750):
        LED_pin.value(1)
        global file_names
        print('Reading Data from manual interrupt...')
        record_values(file_names)
        debounce_time = time.ticks_ms()
        print("saved manually collected data")
        LED_pin.value(0)
        
def button_interrupt_setup(pin):
    pin.irq(trigger=machine.Pin.IRQ_RISING, handler=manual_data_read)
    
def data_collection_loop():
    
    print("Imports and pin setup successful")

    button_reading = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_DOWN)
    button_interrupt_setup(button_reading)

    # global file_name
    global CO2_power_pin
    global VOC_power_pin
    global LED_pin

    LED_pin.value(0)
    
    try:
        while True:
            print('##########')
            LED_pin.value(1)
            record_values(file_names)
            
            print("Values recorded, now delaying...")
            LED_pin.value(0)
            time.sleep(5) # read sensor data every 15 min
    except KeyboardInterrupt:
        CO2_power_pin.value(0)
        VOC_power_pin.value(0)
        LED_pin.value(0)
        print("Exited Successfully")

if __name__ == "__main__":    
    
    CO2_reading_pin, CO2_power = readCO2.setup_pins()
    VOC_power, VOC_reading_pin = readVOC.setup_pins()
    print('CO2 power - Reading: {} - {}'.format(CO2_power, CO2_reading_pin))
    
    
    # print('warming up...(for 20 seconds     )')
    # time.sleep(20)
    data_collection_loop()
