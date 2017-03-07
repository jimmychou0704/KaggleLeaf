import numpy as np
from scipy.optimize import bisect

class BoxCount:
    def __init__(self, pixels):
        self.pixels = pixels
        self.height, self.width = pixels.shape
        self.counts = np.zeros(6, dtype = 'uint')
        self.v_countsindex = np.vectorize(self.countsindex, otypes = 'B')

        self.variation_minarea = np.zeros(6)
        self.l2square_minarea = np.zeros(6)
        midpts = self.midpts_minarea()
        for i in range(6):
            self.variation_minarea[i] = self.variationbox(i, midpts) 
            self.l2square_minarea[i] = self.l2squarebox(i, midpts)
        self.variation_minarea = np.array(self.variation_minarea)
        self.l2square_minarea = np.array(self.l2square_minarea)

    def midpts_minarea(self):
        midptvalues = np.zeros(6)
        
        # Case of all zero corners just gives 0 midpoint value.
        # So no need to compute midptvalues[0]

        # Case of one non-zero corner.

        def f(x):
            result = (2*x - 1) / np.sqrt(1 + (1 - x)**2 + x**2 )
            result += 2*x / np.sqrt( 1 + 2 * x**2)
            return result
        midptvalues[1] = bisect(f, 0, 1) 

        # Case of two non-zero corners on diagonal. 
        # Calculation gives a simple value of 1/2.

        midptvalues[2] = 0.5

        # Case of two non-zero corners on adjacent corners (ie non-diagonal)

        def f(x):
            result = (4*x - 2) / np.sqrt(1 + ( 1 - x )**2 + x**2 )
            result += 2 * x / np.sqrt( 1 + 2 * x**2 )
            result += ( 2 * x - 2 ) / np.sqrt( 1 + 2 * ( 1 - x )**2)
            return result

        midptvalues[3] = bisect(f, 0, 1)

        # Case of three non-zero corners.
        # Calculation shows that it is 1 - case for one corner.

        midptvalues[4] = 1 - midptvalues[1]

        # Case of four non-zero corners.
        # Simply just 1 since this is constant function.

        midptvalues[5] = 1

        return midptvalues

    def variationtriangle(self, right, acute1, acute2):
        variation =  (acute1 - right)**2 + (acute2 - right)**2
        variation = np.sqrt(variation) 
        return variation

    def l2squaretriangle(self, right, acute1, acute2):
        l2square = right**2 + acute1**2 + acute2**2
        l2square += right * acute1 + right * acute2 + acute1 * acute2
        l2square /= 12.0
        return l2square

    def variationbox(self, case, midpts):
        if case == 0:
            return 0
        elif case == 1:
            variation = self.variationtriangle(midpts[1], 1, 0) * 2
            variation += self.variationtriangle(midpts[1], 0, 0) * 2
            return variation

        # Case of two non-zero on diagonals
        elif case == 2:
            variation = self.variationtriangle(midpts[2], 1, 0) * 4 
            return variation

        elif case == 3:
            variation = self.variationtriangle(midpts[3], 1, 0) * 2
            variation += self.variationtriangle(midpts[3], 1, 1)
            variation += self.variationtriangle(midpts[3], 0, 0)
            return variation


        elif case == 4:
            variation = self.variationtriangle(midpts[4], 1, 1) * 2
            variation += self.variationtriangle(midpts[4], 1, 0) * 2
            return variation

        else:
            return 0

    def l2squarebox(self, case, midpts):
        if case == 0:
            return 0
        elif case == 1:
            l2square = self.l2squaretriangle(midpts[1], 1, 0) * 2
            l2square += self.l2squaretriangle(midpts[1], 0, 0) * 2
            return l2square

        # Case of two non-zero on diagonals
        elif case == 2:
            l2square = self.l2squaretriangle(midpts[2], 1, 0) * 4 
            return l2square

        elif case == 3:
            l2square = self.l2squaretriangle(midpts[3], 1, 0) * 2
            l2square += self.l2squaretriangle(midpts[3], 1, 1)
            l2square += self.l2squaretriangle(midpts[3], 0, 0)
            return l2square


        elif case == 4:
            l2square = self.l2squaretriangle(midpts[4], 1, 1) * 2
            l2square += self.l2squaretriangle(midpts[4], 1, 0) * 2
            return l2square

        else:
            return self.l2squaretriangle(1, 1, 1) * 4 


    def getratio_minarea(self):
        variation = np.sum( self.counts * self.variation_minarea )
        l2norm = np.sum( self.counts * self.l2square_minarea ) 
        l2norm = np.sqrt( l2norm )
        return variation / l2norm

    def setpixeldata(self, pixels):
        self.pixels = pixels

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
        boxes = self.v_countsindex(upleft, upright, downleft, downright)

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

