import time

class Timer:
    def __init__(self, timer=1.0, delegate=lambda: print("DELEGATE")):
        self.timer = timer
        self.delegate = delegate
        self.__lastTick = time.time()
        self.__backupTimer = self.timer
        self.__wasCalling = False

    def Update(self):
        if (self.timer > 0): self.timer -= (time.time() - self.__lastTick)
        elif (self.timer <= 0 and not self.__wasCalling):
            self.__wasCalling = True
            self.timer = 0
            self.delegate()
        
        self.__lastTick = time.time()
    
    def Restart(self):
        self.timer = self.__backupTimer
        self.__wasCalling = False

"""
timer = Timer(2)
while True:
    timer.Update()
    time.sleep(0.1)
"""

