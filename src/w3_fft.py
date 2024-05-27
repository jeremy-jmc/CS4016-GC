# Fast Fourier Transform/Transformada de Fourier

"""
https://numpy.org/doc/stable/reference/routines.fft.html
https://docs.scipy.org/doc/scipy/tutorial/fft.html

https://towardsdatascience.com/fourier-transform-the-practical-python-implementation-acdd32f1b96a
https://medium.com/ntust-aivc/opencv-fourier-transform-d9811aaac2d5
https://medium.com/the-modern-scientist/the-fourier-transform-and-its-application-in-machine-learning-edecfac4133c


https://homepages.inf.ed.ac.uk/rbf/HIPR2/fourier.htm
https://www.cs.unm.edu/~brayer/vision/fourier.html

https://github.com/adenarayana/digital-image-processing
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from numba import jit, prange

img : np.ndarray = cv2.imread('../img/lenna.png')     # read in BGR by default
img = cv2.resize(img, (1024, 1024))
img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# https://www.geeksforgeeks.org/how-to-find-the-fourier-transform-of-an-image-using-opencv-python/
# https://towardsdatascience.com/image-processing-with-python-application-of-fourier-transformation-5a8584dc175b


@jit(nopython=True)
def filter(img: np.array, cut_off: int = 50, low: bool = True) -> np.array:
    height, width = img.shape

    filter_array = np.zeros(img.shape, dtype=np.float32)

    for i in prange(height):
        for j in prange(width):
            if np.sqrt((i - height//2)**2 + (j - width//2)**2) < cut_off:
                filter_array[i, j] = 1 if low else 0
            else:
                filter_array[i, j] = 0 if low else 1
    
    return filter_array


def inverse_fourier(img: np.array) -> np.array:
    fshift = np.fft.ifftshift(img)  # N lg N
    img_back = np.abs(np.fft.ifft2(fshift))

    return img_back

# * convert image to frequency domain
f = np.fft.fft2(img_bw)
print(f.shape)

fshift = np.fft.fftshift(f)
img_fft_shifted = np.log1p(np.abs(fshift))

# plot results
plt.figure(figsize=(12, 4))
plt.subplot(131), plt.imshow(img_bw, cmap='gray'), plt.axis('off')
plt.title('original image')
plt.subplot(132), plt.imshow(np.log1p(np.abs(f)), cmap='gray'), plt.axis('off')
plt.title('power spectrum')
plt.subplot(133), plt.imshow(img_fft_shifted, cmap='gray'), plt.axis('off')
plt.title('shifted low frequencies')
plt.xticks([]), plt.yticks([])
plt.show()

# * convert image back to spatial domain
img_back = inverse_fourier(fshift)

cut_off_low = 5
cut_off_high = 5
low_filter = filter(fshift, cut_off_low, True)
high_filter = filter(fshift, cut_off_high, False)


# plot filters
plt.figure(figsize=(12, 4))
plt.subplot(131), plt.imshow(img_back, cmap='gray'), plt.axis('off')
plt.title('original image')
plt.subplot(132), plt.imshow(low_filter, cmap='gray'), plt.axis('off')
plt.title(f'low pass filter cut_off {cut_off_low}')
plt.subplot(133), plt.imshow(high_filter, cmap='gray'), plt.axis('off')
plt.title(f'high pass filter cut_off {cut_off_high}')
plt.xticks([]), plt.yticks([])
plt.show()

img_low_filter = inverse_fourier(fshift * low_filter)
img_high_filter = inverse_fourier(fshift * high_filter)

# plot results
plt.figure(figsize=(12, 4))
plt.subplot(131), plt.imshow(img_back, cmap='gray'), plt.axis('off')
plt.title('original image')
plt.subplot(132), plt.imshow(img_low_filter, cmap='gray'), plt.axis('off')
plt.title(f'low pass filter result: {cut_off_low}')
plt.subplot(133), plt.imshow(img_high_filter, cmap='gray'), plt.axis('off')
plt.title(f'high pass filter result: {cut_off_high}')
plt.xticks([]), plt.yticks([])
plt.show()



"""
low pass filters:
    remove high frequencies
    blurred the image

high pass filters:


complexity of FFT: N lg N

GPU: spatial domain >>>> frequency domain
CPU: frequency domain >>>> spatial domain


FFT is a DFT optimized

Computational Geometry

PC1
    a partir de las 12
"""