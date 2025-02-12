from navigation.rc import RCLib
from navigation.ac import ACLib
import time
import navigation.imu as imu

rc = RCLib()
ac = ACLib()

rc.setmode('MANUAL')

rc.arm()

print(rc.getDeg())

# global "origin" parameter
START = 239
DEPTH_SEC = 5.2
SEC_PER_METER = 1
GATECENTER = 2500
def leftAlign(value) :

    pingReturn = ac.get_distance_fwd()
    wallDist = pingReturn[0]
    confidence = pingReturn[1]
    counter = 0
    while ((confidence < 90) and (counter < 50)):
        pingReturn = ac.get_distance_fwd()
        wallDist = pingReturn[0]
        confidence = pingReturn[1]
        counter = counter + 1
    print 'wall' , wallDist 
    if wallDist > 3800:
        wallDist = 3800
    if wallDist <  500:
        wallDist = 500
    print 'wall' , wallDist 
    print 'counter ' , counter 
    diff =  value - wallDist
    print 'Laterl diff ' , diff
    rc.lateralDist(diff)

def rightAlign(value) :
    pingReturn = ac.get_distance_right()
    wallDist = pingReturn[0]
    confidence = pingReturn[1]
    counter = 0
    while ((confidence < 90) and (counter < 50)):
        pingReturn = ac.get_distance_right()
        wallDist = pingReturn[0]
        confidence = pingReturn[1]
        counter = counter + 1
    print 'wall' , wallDist 
    if wallDist > 3800:
        wallDist = 3800
    if wallDist <  500:
        wallDist = 500
    print 'wall' , wallDist 
    print 'counter ' , counter 
    diff =   wallDist - value
    print 'Laterl diff ' , diff
    rc.lateralDist(diff)


# depth hold and go down
rc.setmode('ALT_HOLD')
rc.throttle("time", DEPTH_SEC, -0.25)

# align with the origin 
rc.imu_turn(START)

rc.forward("time", 10, 0.32)
leftAlign(2400)
rc.imu_turn(START)
rc.forward("time", 5, 0.32)
leftAlign(2000)
rc.imu_turn(START)
rc.forward("time", 5, 0.32)
leftAlign(1500)
rc.imu_turn(START)
rc.forward("time", 5, 0.32)
leftAlign(1500)
rc.forward("time", 5, 0.32)
leftAlign(3500)

rc.imu_turn(85)
rc.forward("time", 15, 0.25)
rc.imu_turn(85)
rightAlign(2500)
rc.imu_turn(85)
rc.forward("time", 8, 0.32)
rightAlign(2500)
rc.imu_turn(80)
rc.throttle("time", 1, -0.25)
rc.forward("time", 3, 0.35)
rightAlign(2500)
rc.imu_turn(80)
rc.forward("time", 10, 0.32)

rc.close()
