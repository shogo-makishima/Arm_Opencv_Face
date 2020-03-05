from cv2 import CascadeClassifier, VideoCapture, cvtColor, COLOR_BGR2GRAY, rectangle, imencode
from Classes.Settings import Settings
import base64


class Main:
    def __init__(self):
        self.Start()

    def Start(self):
        self.face_cascade = CascadeClassifier(f"Files/{Settings.cascade}")
        self.cap = VideoCapture(Settings.capIndex)

    def GetImage(self):
        _, image = self.cap.read()
        gray = cvtColor(image, COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, Settings.scaleFactor, Settings.minNeighbors)

        for (x, y, w, h) in faces:
            if (w * h < Settings.minArea): continue
            else: rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return image

    def ImageToBase64(self, image=None) -> str:
        retval, buffer = imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer)
        return jpg_as_text
