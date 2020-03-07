from cv2 import CascadeClassifier, VideoCapture, cvtColor, COLOR_BGR2GRAY, rectangle, imencode
from Classes.Settings import Settings
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

        asyncio.run(self.Start())

        self.loopThread = threading.Thread(target=self.MainLoop)
        self.loopThread.start()

    async def Start(self) -> None:
        self.face_cascade = CascadeClassifier(f"Files/{Settings.cascade}")
        self.cap = VideoCapture(Settings.capIndex)
        if (Settings.port): self.serialArduino = serial.Serial(port=Settings.port, baudrate=9600)        

    def GetImage(self): return self.image

    def ImageToBase64(self, image=None) -> str:
        retval, buffer = imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer)
        return jpg_as_text

    @threadsafeFunction
    def MainLoop(self):
        while True:
            if (not self.cap and not self.face_cascade): continue
            _, self.image = self.cap.read()
            gray = cvtColor(self.image, COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, Settings.scaleFactor, Settings.minNeighbors)
            
            if (len(faces) == 0):
                if (self.serialArduino): self.serialArduino.write(bytes("n", encoding="utf-8"))
                continue

            for (x, y, w, h) in faces:
                if (w * h < Settings.minArea): continue
                else: 
                    if (self.serialArduino): self.serialArduino.write(bytes("d", encoding="utf-8"))
                    rectangle(self.image, (x, y), (x + w, y + h), (255, 0, 0), 2)
