import time
# Import mavutil
from pymavlink import mavutil
import math

# Wait for server connection
def wait_conn(master):
    msg = None
    while not msg:
        master.mav.ping_send(
            time.time(), # Unix time
            0, # Ping number
            0, # Request ping of all systems
            0 # Request ping of all components
        )
    msg = master.recv_match()
    time.sleep(0.5)
    
master = mavutil.mavlink_connection('/dev/ttyACM0', baud=115200)

#wait_conn(master)

while True:
    try:
        att_val = (master.recv_match(type='ATTITUDE').to_dict())
        yaw = att_val['yaw']
        yaw_deg = math.floor(yaw * (180/3.1415926535))
        print(yaw_deg)
    except:
        time.sleep(0.1)
        print('In Loop')
