class Settings:
    cascade: str = "haarcascade_frontalface_default.xml"
    resolution: tuple = (1280, 720)
    capIndex: int = 0

    port: str = None

    key: str = "What314.5Color?"

    scaleFactor: float = 1.3
    minNeighbors: int = 8

    minArea: int = 25000

    def SetSetting(self, getScaleFactor: float = 1.3, getMinNeighbors: int = 8, getMinArea: int = 25000, getCapIndex: int = 0, getCascade: str = "haarcascade_frontalface_default.xml", getPort: str = "COM6") -> None:
        self.scaleFactor = getScaleFactor
        self.minNeighbors = getMinNeighbors
        self.minArea = getMinArea
        self.capIndex = getCapIndex
        self.cascade = getCascade
        self.port = getPort