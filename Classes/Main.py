from cv2 import CascadeClassifier, CAP_PROP_FPS, VideoCapture, cvtColor, COLOR_BGR2GRAY, rectangle, imencode, imshow, waitKey
from Classes.Settings import Settings
from Classes.Timer import Timer
import base64, serial, asyncio, threading, time

def threadsafeFunction(func):
    lock = threading.Lock()
    def new(*args, **kwargs):
        lock.acquire()
        try: r = func(*args, **kwargs)
        except Exception as e: raise e
        finally: lock.release()
        return r
    return new


class Main:
    def __init__(self):
        self.image = None
        self.loopThread: threading.Thread = None
        self.face_cascade: CascadeClassifier = None
        self.cap: VideoCapture = None
        self.serialArduino: serial.Serial = None

        self.timerCanSendData: bool = True
        self.timer: Timer = Timer(Settings.timerPause, lambda: self.SetCanSendData(True))

        asyncio.run(self.Start())
        
        self.loopThread = threading.Thread(target=self.MainLoop)
        self.loopThread.daemon = True
        self.loopThread.start()

        if (Settings.showWindow):
            self.cameraThread = threading.Thread(target=self.CameraOut)
            self.cameraThread.daemon = True
            self.cameraThread.start()


    async def Start(self) -> None:
        self.face_cascade = CascadeClassifier(f"Files/{Settings.cascade}")
        if (not self.cap):
            self.cap = VideoCapture(Settings.capIndex)
            self.cap.set(3, Settings.resolution[0])
            self.cap.set(4, Settings.resolution[1])

        if (Settings.port): 
            if (self.serialArduino): self.serialArduino.close()
            self.serialArduino = serial.Serial(port=Settings.port, baudrate=Settings.speed)

    def GetImage(self): return self.image

    def ImageToBase64(self, image=None) -> str:
        retval, buffer = imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer).decode("ascii")
        return jpg_as_text

    def CameraOut(self):
        while True:
            if (self.image is not None):
                imshow("Image", self.image)
                waitKey(25)
    
    def SetCanSendData(self, value: bool = False): self.timerCanSendData = value


    def MainLoop(self):
        while True:
            self.timer.Update()

            if (not self.cap and not self.face_cascade): continue
            _, self.image = self.cap.read()
            gray = cvtColor(self.image, COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, Settings.scaleFactor, Settings.minNeighbors)            

            if (not self.timerCanSendData): continue
            
            if (len(faces) == 0):
                self.timer.Restart(); self.SetCanSendData(False)
                if (self.serialArduino): self.serialArduino.write(bytes("n", encoding="utf-8"))
                continue

            for (x, y, w, h) in faces:
                self.timer.Restart(); self.SetCanSendData(False)
                if (w * h < Settings.minArea): continue
                else: rectangle(self.image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                if (self.serialArduino):  self.serialArduino.write(bytes("d", encoding="utf-8"))