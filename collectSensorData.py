
if __name__ == "__main__":
    
    try:
        import machine
        import time
        import readCO2
        import readOnboardTemp
        import readPM2_5
        import readVOC
    except:
        raise ValueError("Error importing files (make sure everything being imported is flashed onto the pi)")
    
    CO2_power_pin, CO2_reading_pin = readCO2.setup_pins()
    VOC_power_pin, VOC_reading_pin = readVOC.setup_pins()
    print("Imports and pin setup successful")
    
    # TODO create file
    
    # TODO read all required sensor data into file
    
    # TODO sleep for variable time
    
    # TODO format as function with if main thing so we can call seperately later

    # TODO save sensor values on manual button press
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        CO2_power_pin.value(0)
        VOC_power_pin.value(0)
        print("Exited Successfully")
