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
        rightindex = rightvertex
        acuteindex = acute1 + acute2
        self.counts[rightindex][acuteindex] += 1
       

    def getcounts(self, step = 1):
        self.counts = np.zeros((2,3), dtype = 'uint')
#         for i in range(0, self.height - 1, step):
#            itup = self.pixels[i][ :-1:step]
#            itright = self.pixels[i][ 1::step]
#            itdown = self.pixels[i+1][ :-1:step]
#            itdownright = self.pixels[i+1][ 1::step]
#            for acute1, right1, acute2, right2 in np.nditer([itup, itright, itdown, itdownright]):
#                self.updatecounts( int(right1)
#                                 , int(acute1)
#                                 , int(acute2)
#                                 )
#                self.updatecounts( int(right2)
#                                 , int(acute1)
#                                 , int(acute2)
#                                 )
# 

           
        for i in range(0, self.height - 1, step):
            for j in range(0, self.width - 1, step): 
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
