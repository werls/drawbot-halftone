from drawBot import BezierPath, drawPath

def map_range(value, start1, stop1, start2, stop2):
    return (value - start1) / (stop1 - start1) * (stop2 - start2) + start2

class Tile:
    def __init__(self, width, height, radius = 1):
        self.width = width
        self.height = height
        self.radius = radius
        self.path = BezierPath()
        
        if self.radius == 0:
            self.f = 1
        else:
            self.f = self.width / map_range(radius, 3, -3, 0, self.width)
        
    def setPath(self, x, y):
        self.path.moveTo((x, y + self.height / self.f))
        self.path.lineTo((x, y + self.height - self.height / self.f))
        self.path.lineTo((x + self.width / self.f, y + self.height))
        self.path.lineTo((x + self.width - self.width / self.f, y + self.height))
        self.path.lineTo((x + self.width, y + self.height - self.height / self.f))
        self.path.lineTo((x + self.width, y + self.height / self.f))
        self.path.lineTo((x + self.width - self.width / self.f, y))
        self.path.lineTo((x + self.width / self.f, y))
        self.path.lineTo((x, y + self.height / self.f))
                
    def drawPath(self):
        drawPath(self.path)