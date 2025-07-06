import threading, websocket
import time, math

#pip install websocket-client


class Robot:
    def __init__(self, host="localhost", port=5080, arm=147.5, robotNr = 0):
        self.isRunning = True
        self.arm = arm
        self.robotNr = robotNr
        self.MotorX = 0.0
        self.MotorY = 0.0
        self.MotorZ = 0.0
        self.CoordX = 0.0
        self.CoordY = 0.0
        self.CoordZ = 0.0


        self.feed = 3000
        self.lastPing = time.time()
        print("Start-Time:" + str(self.lastPing))

        self.ws = websocket.WebSocket()
        self.ws.connect(f"ws://{host}:{port}")
        self.rec_thread = threading.Thread(target=self.receiver)
        self.rec_thread.start()
        time.sleep(0.1)
        self.ws.send("?\n")
        self.ping_thread = threading.Thread(target=self.send_ping)
        self.ping_thread.start()

        if(robotNr > 0):
            print("Change to diffrent Simulation! not suitable for the real FluidNC Robot." )
            self.ws.send("simNr="+str(robotNr)+"\n")

        time.sleep(0.05)

    def close(self):
        self.isRunning = False
        self.ws.close()
        self.rec_thread.join()
        self.ping_thread.join()

    # Reception needs to be done in a separate thread; you cannot
    # assume that a given command will always result in exactly one
    # response at a predictable time
    def receiver(self):
        while self.isRunning:
            for l in self.ws.recv().splitlines():
                if isinstance(l, str):
                    #print(l)
                    self.processResponse(l)
                else:
                    #print(str(l, 'utf-8'))
                    self.processResponse(str(l, 'utf-8'))

    def send(self, msg):
        if(not str(msg).endswith('\n')):
           print("Command should end with the Newline Character")
           msg = str(msg) + '\n'

        print("send: " + str(msg)  + " to Status " + str(self.ws.status))
        self.ws.send(msg)
        print("send seems OK " + str(self.ws.status))

    def send_ping(self):
        while self.isRunning:
            self.ws.send("?\n")
            for _ in range(100):
                if(not self.isRunning):
                    break
                time.sleep(0.04)

    
    def calculateMotor(self):

        r = math.sqrt(self.CoordZ**2 + self.CoordY**2)
        
        if(r == 0):
            print("Divided by Zero!!!!")
            return
        
        phi = math.asin(self.CoordZ/r)

        if(self.CoordY < 0): phi = math.pi - phi

        if(r  > 2* self.arm):
            print("Coordinates can not be reached. Input is ignored.")
            return
        

        EllbogenWinkel = math.acos((2*((self.arm)**2)-(r)**2)/(2*((self.arm)**2)))
        MotorXminusPhi =  math.acos(((r)**2)/(2*self.arm*r))

        self.MotorZ = ((MotorXminusPhi) + (phi)) * 180.0 / (math.pi)
        self.MotorY = -(180  - self.MotorZ  - EllbogenWinkel*180/math.pi)

        self.MotorX = self.CoordX
                

    def gotoMotorXYZ(self, newMotorX, newMotorY, newMotorZ, feed = 5000):
        self.MotorX = newMotorX
        self.MotorY = newMotorY
        self.MotorZ = newMotorZ
        
        
        #self.CoordY = math.cos(newMotorX*math.pi/180)*self.arm + math.cos(newMotorZ*math.pi/180)*self.arm
        #self.CoordZ = math.sin(newMotorX*math.pi/180)*self.arm + math.sin(newMotorZ*math.pi/180)*self.arm

        print("G1 x" +str(self.MotorX)+ " y"+str(self.MotorY) +" z"+str(self.MotorZ) + " f"+str(feed) + ' \n')
        self.send("G1 x" +str(self.MotorX)+ " y"+str(self.MotorY) +" z"+str(self.MotorZ) + " f"+str(feed) + ' \n')

    def gotoCoordXYZ(self, x=None, y=None, z=None, feed=4000):
        
        if(x == None):
            x = self.CoordX
        if(y == None):
            y = self.CoordY
        if(z == None):
            z = self.CoordZ
        if(feed != 4000):
            self.feed = feed

        print("Koordinatein: x=" + str(x) +" y=" + str(y) +" z=" + str(z) )
            
        self.calculateMotor()
        self.gotoMotorXYZ(newMotorX=self.MotorX, newMotorY=self.MotorY, newMotorZ=self.MotorZ, feed=self.feed)

    def processResponse(self, response):
        if("ERR" in response):
            print("From Robot: " + response)

        return

        if("{" not in response and ":" in response and "," in response):
            xyz = response.split(":")[1].split("|")[0].split(",")

            print("Process Response: " + str(xyz))
            if(len(xyz) < 2):
                print("Unerwartete Antwort vom Roboter")
                return

            self.MotorX = float(xyz[0])
            self.MotorY = float(xyz[1])
            self.MotorZ = float(xyz[2])

            print("Response OK")

            #self.CoordX = math.cos(self.MotorX*math.pi/180)*self.arm + math.cos(self.MotorZ*math.pi/180)*self.arm
            #self.CoordY = math.sin(self.MotorX*math.pi/180)*self.arm + math.sin(self.MotorZ*math.pi