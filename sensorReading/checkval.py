acceptable_val_ranges = {
    "CO2": {"Lower": 0, "Upper": 1000}, 
    "Temperature":{"Lower":20, "Upper":30},
    "PM2_5":{"Lower":0, "Upper":14}, 
    "VOC":{"Lower":0, "Upper":0.5}, "Humidity":{"Lower":30, "Upper":60}
    }

def checkval(data,acceptable_val_ranges=acceptable_val_ranges):
    acceptable_values = {}
    not_acceptable_values = {}

    for sensor, value in data.items():
        if sensor in acceptable_val_ranges:
            lower = acceptable_val_ranges[sensor]["Lower"]
            upper = acceptable_val_ranges[sensor]["Upper"]
            if lower <= value <= upper:
                acceptable_values[sensor] = value
            else:
                not_acceptable_values[sensor] = value
        else:
            # For sensors without defined ranges, consider them not acceptable
            not_acceptable_values[sensor] = value

    return acceptable_values, not_acceptable_values