class Settings:
    cascade: str = "haarcascade_frontalface_default.xml"
    resolution: tuple = (320, 240)
    capIndex: int = 0

    showWindow: bool = True
    port: str = None
    speed: int = 9600

    timerPause: float = 0.2

    key: str = "What314.5Color?"

    scaleFactor: float = 1.3
    minNeighbors: int = 8

    minArea: int = 10000

    def SetSetting(self, getScaleFactor: float = 1.3, getMinNeighbors: int = 8, getMinArea: int = 25000, getCapIndex: int = 0, getCascade: str = "haarcascade_frontalface_default.xml", getPort: str = "COM6") -> None:
        self.scaleFactor = getScaleFactor
        self.minNeighbors = getMinNeighbors
        self.minArea = getMinArea
        self.capIndex = getCapIndex
        self.cascade = getCascade
        self.port = getPort
