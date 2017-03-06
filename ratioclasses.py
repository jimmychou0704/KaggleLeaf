import numpy as np

class BoxCount:
    def __init__(self, pixels):
        self.pixels = pixels
        self.height, self.width = pixels.shape
        self.counts = np.zeros(6, dtype = 'uint')

    # Index of self.counts -> Type of Non-zero corner count
    # 0 -> 0 Count
    # 1 -> 1 Count
    # 2 -> 2 Count, Diagonals
    # 3 -> 2 Count, Non-diagonals
    # 4 -> 3 Count
    # 5 -> 4 Count

    # We model the function as piecewise linear in each block, where the function is linear
    # on 4 regular interior triangles. We assume the value of the function in the middle is
    # arithmetic average of four corners.

    def findperimeter(self):
        L1gradients = [ 0.0
                      , np.sqrt( 0.25**2 + 0.75**2 ) * 0.5 + np.sqrt( 0.25**2 + 0.25**2) * 0.5 
                      , np.sqrt( 0.5**2 + 0.5**2 ) 
                      , np.sqrt( 0.5**2 + 0.5**2 ) 
                      , np.sqrt( 0.25**2 + 0.75**2 ) * 0.5 + np.sqrt( 0.25**2 + 0.25**2 ) * 0.5
                      , 0.0
                      ]
        L1gradients = np.array(L1gradients)

        perimeter = np.sum(L1gradients * self.counts)
        return perimeter


    def L2Triangle(self, right, acute1, acute2):
        result = right**2 + acute1**2 + acute2**2
        result += right * acute1 + acute1 * acute2 + right * acute2
        result /= 12.0
        return result

    def findL2Norm(self):
        L2squares = [ 0.0
                    , self.L2Triangle(0.25, 1.0, 0.0) * 2 + self.L2Triangle(0.25, 0.0, 0.0) * 2
                    , self.L2Triangle(0.5, 1.0, 0.0) * 4
                    , self.L2Triangle(0.5, 1.0, 1.0) + self.L2Triangle(0.5, 0.0, 1.0) * 2 + self.L2Triangle(0.5, 0.0, 0.0)
                    , self.L2Triangle(0.75, 1.0, 1.0) * 2 + self.L2Triangle(0.75, 1.0, 0.0) * 2
                    , self.L2Triangle(1.0, 1.0, 1.0) * 4  
                    ]
        L2squares = np.array(L2squares)
        L2norm = np.sum( L2squares * self.counts )
        L2norm = np.sqrt( L2norm )
        return L2norm

    def countsindex(self, upleft, upright, downleft, downright):
        countnonzero = upleft + upright + downleft + downright
        if countnonzero == 0:
            return 0
        elif countnonzero == 1:
            return 1
        elif countnonzero == 2:
            if upleft == 1 and downright == 1:
                return 2
            elif upright == 1 and downleft == 1:
                return 2
            else:
                return 3
        elif countnonzero == 3:
            return 4
        else:
            return 5

    def getcounts(self):
        upleft = self.pixels[:-1, :-1]
        upright = self.pixels[:-1, 1:]
        downleft = self.pixels[1:, :-1]
        downright = self.pixels[1:, 1:]
        v_countsindex = np.vectorize(self.countsindex)
        boxes = v_countsindex(upleft, upright, downleft, downright)

        boxtype, counts = np.unique(boxes, return_counts = True)
        self.counts = np.zeros(6, dtype = 'uint')
        for i in range(len(boxtype)):
            self.counts[boxtype[i]] = counts[i]
        


class TriangleCount:
    def __init__(self, pixels):
        self.pixels = pixels
        self.height, self.width = pixels.shape
        self.counts = np.zeros((2,3), dtype = 'uint')

    def normalize(self):
        self.pixels[self.pixels > 0] = 1

    def updatecounts(self, rightvertex, acute1, acute2):
        rightindex = rightvertex
        acuteindex = acute1 + acute2
        self.counts[rightindex][acuteindex] += 1

    def updatecountsnumeric(self, values, counts):
        for i in range(len(values)):
            if values[i] > 9:
                rightindex = 1
            else: 
                rightindex = 0
            acuteindex = values[i] % 10
            self.counts[rightindex][acuteindex] += counts[i] 
       

    def getcounts(self, step = 1):
        self.counts = np.zeros((2,3), dtype = 'uint')
 
        acute1 = self.pixels[:-1, :-1]
        acute2 = self.pixels[1:, 1:]
        right = self.pixels[:-1, 1:]
        triangles = 10*right + acute1 + acute2
        triangles, counts = np.unique(triangles, return_counts = True)
        self.updatecountsnumeric(triangles, counts)

        right = self.pixels[1:, :-1]
        triangles = 10*right + acute1 + acute2
        triangles, counts = np.unique(triangles, return_counts = True)
        self.updatecountsnumeric(triangles, counts)

