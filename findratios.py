from PIL import Image
import PIL.ImageOps
import numpy as np
import ratioclasses as rc 
import time
import matplotlib.pyplot as plt

outputname = 'ratiostest.csv'
seperator = '\n-------------------------\n'

# The gradient weights for L1 norm of gradient for each triangle type
gradientsize = [ [np.sqrt(j) for j in range(3)]
               , [np.sqrt(2 - j) for j in range(3)]
               ]
gradientsize = np.array( gradientsize )
gradientsize *= 1.0/2.0
print(seperator, 'gradientsize = \n', gradientsize )

# The weights for L2 norm of each triangle type. To be applied before
# square root.
L2size = [ [0.0, 1/12.0, 11/36.0]
         , [1.0/12.0, 1/4.0, 1/2.0]
         ]
L2size = np.array(L2size)
print('L2size = \n', L2size)

numpics = 1584
# numpics = 500

isopratios = np.zeros((numpics, 2))
lasttime = time.clock()
for i in range(numpics):
    
    # Load the image.
    filename = 'Data/images/' + str(i+1) + '.jpg' 
    myimage = Image.open(filename)
    myimage = myimage.convert('1')
    #(imheight, imwidth) = myimage.size
    (imwidth, imheight) = myimage.size
    
    pixeldata = np.array(myimage.getdata(), dtype = 'uint')
    pixeldata = pixeldata.reshape(imheight, imwidth)
    
    # Set up counter. Normalize the pixel data to be values of 0 or 1.
    # pixeldata = np.floor_divide(pixeldata, 255)
    pixeldata[pixeldata > 0] = 1
    counter = rc.TriangleCount(pixeldata)
    # counter.normalize()
    counter.getcounts(step = 1)
    
    totalgradient = np.sum( counter.counts * gradientsize ) 
    L2norm = np.sum( counter.counts * L2size)
    L2norm = np.sqrt( L2norm )
    ratio = totalgradient / L2norm

    isopratios[i][0] = i + 1
    isopratios[i][1] = ratio
    myimage.close()
    currenttime = time.clock()
    if currenttime - lasttime > 20: 
        print(seperator, 'Finished analyzing image ', filename)
        print('Triangle Counts = \n', counter.counts)
        print('Ratio = ', ratio)
        lasttime = currenttime
    
print('Now Saving Results to file ', outputname)
f = open(outputname, 'w')
f.truncate()
line = 'id,isopratio\n'
f.write(line)
for i in range(numpics):
    line = str(i+1) + ',' + str(isopratios[i][1]) +  '\n'
    f.write(line)
f.close()
    
#################### Old Stuff
perimetersize = [ [0, 1, 2]
                , [2, 1, 0]
                ]

L1size = [ [0.0, 1.0/6.0, 2.0/6.0]
         , [1.0/2.0 - 2.0/6.0, 1.0/2.0 - 1.0/6.0, 1.0/2.0] 
         ] 
L1size = np.array( L1size )

