
import sensors
import server
import localdb
import time
from timeloop import Timeloop
from datetime import timedelta

# Initialize Raspberry Pi and Room IDs
rpi_id = "m1"
room_id = "r1"

# Initialize Timeloop
time_loop = Timeloop()

# Set time intervals for data storage in local and central servers
LOCAL_SERVER_TIME_INTERVAL = 60 # seconds
CENTRAL_SERVER_TIME_INTERVAL = 3600 # seconds

@time_loop.job(interval=timedelta(seconds=LOCAL_SERVER_TIME_INTERVAL))
def localdb_routine():
    try:
        reading = sensors.get_reading(rpi_id, room_id)
        localdb.store_data(reading)
    except:
        print("Exception in local_routine")

@time_loop.job(interval=timedelta(seconds=CENTRAL_SERVER_TIME_INTERVAL))
def server_routine():
    last_date_time = server.get_latest_entry(rpi_id, room_id)
    file_name = localdb.extract_to_csv(last_date_time, rpi_id, room_id)
    server.sendFile(file_name)

def initiate_sensors():
    sensors.start_sound_reading()
    sensors.start_vibration_reading()
    sensors.start_motion_reading()
    sensors.start_flame_reading()
    sensors.start_mq2_reading()

def main():
    print("Running Local Module")
    initiate_sensors()
    time_loop.start()

if __name__ == "__main__":
    main()
