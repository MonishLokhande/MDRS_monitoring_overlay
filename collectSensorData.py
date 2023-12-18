def file_name_setup(file_name = 'sensor_log.txt'):
    return file_name

def record_values(file_name):
    print("Recording CO2 values")
    readCO2.record_data(CO2_reading_pin, file_name)
    
    print("Recording VOC values")
    readVOC.record_data(VOC_reading_pin, file_name)
    
    print("Recording temp values")
    readOnboardTemp.record_data(file_name)
    
    print("Recording dust values")
    readPM2_5.record_data(file_name)

if __name__ == "__main__":
    import machine
    import time
    try:
        import readCO2
        import readOnboardTemp
        import readPM2_5
        import readVOC
    except:
        raise ValueError("Error importing files\nMake sure everything being imported is copied onto the pi and named exactly the same as specified in this file")
    
    print("Imports and pin setup successful")
    
    CO2_power_pin, CO2_reading_pin = readCO2.setup_pins()
    VOC_power_pin, VOC_reading_pin = readVOC.setup_pins()

    # TODO save sensor values on manual button press, interrupt tutorial below
    # https://electrocredible.com/raspberry-pi-pico-external-interrupts-button-micropython/
    
    
    file_name = file_name_setup()

    try:
        while True:
            record_values(file_name)
            
            print("Vales recorded, now delaying for an hour...")
            time.sleep(60*60) # read sensor data every hour
    except KeyboardInterrupt:
        CO2_power_pin.value(0)
        VOC_power_pin.value(0)
        print("Exited Successfully")
