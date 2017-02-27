from PIL import Image
import PIL.ImageOps
import numpy as np
import triangle as tr

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

# Load the images.
myimage = Image.open('Data/images/1.jpg')
#myimage = Image.open('circle.jpg')
#myimage = Image.open('othertriangle.jpg')
myimage = myimage.convert('1')
(imheight, imwidth) = myimage.size
print('image dimensions = ', myimage.size)

pixeldata = np.array(myimage.getdata(), dtype = 'uint')
pixeldata = pixeldata.reshape(imheight, imwidth)
print('pixeldata shape = ', pixeldata.shape)

# Set up counter. Normalize the pixel data to be values of 0 or 1.
counter = tr.TriangleCount(pixeldata)
counter.normalize()
print(seperator, 'Pixel Data has been normalized.')
print('Double Check: Max of pixeldata = ', np.max(counter.pixels))
counter.getcounts()
print('Triangle Counts = \n', counter.counts)

totalgradient = np.sum( counter.counts * gradientsize ) 
L2norm = np.sum( counter.counts * L2size)
L2norm = np.sqrt( L2norm )
ratio = totalgradient / L2norm
print(seperator, 'Total Gradient = ', totalgradient)
print('L2norm = ', L2norm )
print('Ratio = ', ratio ) 


#################### Old Stuff
perimetersize = [ [0, 1, 2]
                , [2, 1, 0]
                ]

L1size = [ [0.0, 1.0/6.0, 2.0/6.0]
         , [1.0/2.0 - 2.0/6.0, 1.0/2.0 - 1.0/6.0, 1.0/2.0] 
         ] 
L1size = np.array( L1size )

