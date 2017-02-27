import numpy as np

class TriangleCount:
    def __init__(self, pixels):
        self.pixels = pixels
        self.height, self.width = pixels.shape
        self.counts = np.zeros((2,3), dtype = 'uint')

    def normalize(self):
        for point in np.nditer(self.pixels, op_flags = ['readwrite']):
            if point > 0: 
                point[...] = 1

    def updatecounts(self, rightvertex, acute1, acute2):
        self.counts[rightvertex][acute1 + acute2] += 1

    def getcounts(self):
        self.counts = np.zeros((2,3), dtype = 'uint')
        for i in range(self.height - 1):
            for j in range(self.width - 1): 
                acute1 = self.pixels[i][j]
                acute2 = self.pixels[i+1][j+1]
                self.updatecounts( self.pixels[i+1][j]
                                 , acute1
                                 , acute2
                                 )
                self.updatecounts( self.pixels[i][j+1]
                                 , acute1
                                 , acute2
                                 )
