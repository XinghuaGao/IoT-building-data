
import sensors
import time

def main():
    print("Main function running. Welcome to the system.")
    
    reading_interval = 5 # seconds
    sensors.start_sound_reading()
    sensors.start_vibration_reading()
    sensors.start_motion_reading()
    sensors.start_flame_reading()
    sensors.start_mq2_reading()

    while True:
        readings = {
            "Temp": sensors.get_temperature(),
            "Humidity": sensors.get_humidity(),
            "Light": sensors.get_light(),
            "Sound": sensors.get_sound(),
            "Vibration": sensors.get_vibration(),
            "Motion": sensors.get_motion(),
            "Flame": sensors.get_flame(),
            "LPG": sensors.get_lpg(),
            "CO": sensors.get_co(),
            "Smoke": sensors.get_smoke(),
        }

        for name, value in readings.items():
            print(f"{name}: {value}")

        time.sleep(reading_interval)

if __name__ == "__main__":
    main()
