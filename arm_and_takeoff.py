
from droneapi.lib import VehicleMode
from pymavlink import mavutil
import time

api = local_connect()
vehicle = api.get_vehicles()[0]

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't let the user try to fly autopilot is booting
    if vehicle.mode.name == "INITIALISING":
        print "Waiting for vehicle to initialise"
        time.sleep(1)
        
    while vehicle.gps_0.fix_type < 2:
        print "Waiting for GPS...:", vehicle.gps_0.fix_type
        time.sleep(1)

    #print 'No GPS mode'
    print "Arming motors"
    # Copter should arm in GUIDED mode
    #vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True
    vehicle.flush()

    while not vehicle.armed and not api.exit:
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.flush()
    
    vehicle.commands.takeoff(aTargetAltitude) # Take off to target altitude
    vehicle.flush()

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.commands.takeoff will execute immediately).
    while not api.exit:
        print " Altitude: ", vehicle.location.alt
        if vehicle.location.alt>=aTargetAltitude*0.95: #Just below target, in case of undershoot.
            print "Reached target altitude"
            break;
        time.sleep(1)



'''
Arm the Copter and fly to 3meters height
'''
arm_and_takeoff(3)

tiem.sleep(10)
 
print("Setting LAND mode...")
vehicle.mode = VehicleMode("LAND")
vehicle.flush()

print("Completed")

'''
api start "C:\Program Files (x86)\MAVProxy\examples\arm_and_takeoff.py"
'''
