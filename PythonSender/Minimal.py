from Robot import *
import keyboard
import time


#r = Robot("localhost", 5080, robotNr=1)
r = Robot("fluidNC5Motor.local", 81)
#r = Robot("sim.schooltech.ch", 80)

time.sleep(0.3)
print("............")


#r.send(str("G1 x50 f3200\n"))

r.gotoMotorXYZ(-20,30,0)

time.sleep(3)
print("............")
r.send("?\n")
r.close()
