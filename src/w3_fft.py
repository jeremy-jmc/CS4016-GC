# Fast Fourier Transform/Transformada de Fourier

"""
https://numpy.org/doc/stable/reference/routines.fft.html
https://docs.scipy.org/doc/scipy/tutorial/fft.html

https://towardsdatascience.com/fourier-transform-the-practical-python-implementation-acdd32f1b96a
https://medium.com/ntust-aivc/opencv-fourier-transform-d9811aaac2d5
https://medium.com/the-modern-scientist/the-fourier-transform-and-its-application-in-machine-learning-edecfac4133c


https://homepages.inf.ed.ac.uk/rbf/HIPR2/fourier.htm
https://www.cs.unm.edu/~brayer/vision/fourier.html
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

img : np.ndarray = cv2.imread('../img/lenna.png')     # read in BGR by default
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# https://www.geeksforgeeks.org/how-to-find-the-fourier-transform-of-an-image-using-opencv-python/
# https://towardsdatascience.com/image-processing-with-python-application-of-fourier-transformation-5a8584dc175b

# convert image to frequency domain
f = np.fft.fft2(img_rgb)
print(f.shape)

fshift = np.fft.fftshift(f)
magnitude_spectrum = 20 * np.log(np.abs(fshift))

plt.subplot(121), plt.imshow(img_rgb, cmap='gray')
plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()

# convert image back to spatial domain
f_ishift = np.fft.ifftshift(fshift)
img_back = np.fft.ifft2(f_ishift)
img_back = np.abs(img_back)

plt.subplot(121), plt.imshow(magnitude_spectrum, cmap='gray')
plt.subplot(122), plt.imshow(img_back, cmap='gray')
plt.title('Image after HPF'), plt.xticks([]), plt.yticks([])
plt.show()
