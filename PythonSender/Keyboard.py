from Robot import *
import keyboard
import time


#r = Robot("localhost", 5080, robotNr=1)
r = Robot("fluidnc5motor.local", 81)
hand = Robot("fluidnc5motorA.local", 81)
#r = Robot("sim.schooltech.ch", 80)
#r = Robot("10.98.41.34",5081)
#r = Robot("10.98.41.34",5061)
r.CoordY = 2*r.arm - 2
r.feed = 12000

print()

stepYZ = 5
stepHand = 2
waitYZ = 0.006
waitYZ = 0.01

while True:
    # Wait for key press
    if keyboard.is_pressed('right') or keyboard.is_pressed('l') or keyboard.is_pressed('L'):
        r.CoordX += stepYZ
        r.gotoCoordXYZ()
        time.sleep(waitYZ)
    if keyboard.is_pressed('left') or keyboard.is_pressed('j') or keyboard.is_pressed('J'):
        r.CoordX -= stepYZ
        r.gotoCoordXYZ()
        time.sleep(waitYZ)
    if keyboard.is_pressed('u') or keyboard.is_pressed('U'):
        r.CoordY -= stepYZ
        r.gotoCoordXYZ()
        time.sleep(waitYZ)
    if keyboard.is_pressed('O') or keyboard.is_pressed('O'):
        r.CoordY += stepYZ
        r.gotoCoordXYZ()
        time.sleep(waitYZ)
    if keyboard.is_pressed('up')  or keyboard.is_pressed('i') or keyboard.is_pressed('I'):
        r.CoordZ += stepYZ
        r.gotoCoordXYZ()
        time.sleep(waitYZ)
    if keyboard.is_pressed('down') or keyboard.is_pressed('k') or keyboard.is_pressed('K'):
        r.CoordZ -= stepYZ
        r.gotoCoordXYZ()
        time.sleep(waitYZ)
    if keyboard.is_pressed('m'):
        r.CoordX = 0
        r.CoordY = r.arm
        r.CoordZ = 0
        r.gotoCoordXYZ()
    if keyboard.is_pressed('q') or keyboard.is_pressed('esc'):
       r.gotoMotorXYZ(0,0,0)
       time.sleep(0.4)
       r.close()
       break
    if keyboard.is_pressed('f'):
        hand.MotorX += stepHand
        hand.MotorY -= stepHand
        hand.gotoCoordXYZ()
        time.sleep(waitYZ)
    if keyboard.is_pressed('d'):
        hand.MotorX -= stepHand
        hand.MotorY += stepHand
        hand.gotoCoordXYZ()
        time.sleep(waitYZ)
    if keyboard.is_pressed('r'):
        hand.MotorX -= stepHand
        hand.MotorY -= stepHand
        hand.gotoCoordXYZ(feed=20000)
        time.sleep(waitYZ)
    if keyboard.is_pressed('e'):
        hand.MotorX += stepHand
        hand.MotorY += stepHand
        hand.gotoCoordXYZ(feed=20000)
        time.sleep(waitYZ)