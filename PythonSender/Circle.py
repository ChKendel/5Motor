from Robot import *
import time
import math


r =  Robot("localhost", 5080) 

for t in range(360):
    x = 200 + 80*math.cos(t*math.pi/180)
    y = 80*math.sin(t*math.pi/180)
    print(t,x,y)

    r.gotoCoordXY(x, y)
    time.sleep(0.05)

r.close()