"""
Study and understand how it works the tone mapping, to create HDR images.

https://yanwei-liu.medium.com/image-signal-processing-pipeline-essential-operations-for-enhancing-raw-images-with-numpy-opencv-1788b7e74378
https://towardsdatascience.com/a-simple-hdr-implementation-on-opencv-python-2325dbd9c650
https://medium.com/@muhammedcan.erbudak/ray-tracing-from-scratch-advanced-lighting-hdr-rendering-f4d4eaec59fa
https://videocompressionguru.medium.com/differences-between-hdr-and-sdr-3689aa543725
https://skylum.com/blog/what-is-tone-mapping
https://www.cl.cam.ac.uk/~rkm38/pdfs/tone_mapping.pdf
https://es.wikipedia.org/wiki/Mapeo_de_tonos

keyword: tone mapping python


https://en.wikipedia.org/wiki/Tone_mapping
https://en.wikipedia.org/wiki/High_dynamic_range
https://medium.com/hd-pro/tone-mapping-to-achieve-high-dynamic-range-hdr-2463bf5cd9fa
https://yanwei-liu.medium.com/image-signal-processing-pipeline-essential-operations-for-enhancing-raw-images-with-numpy-opencv-1788b7e74378
https://zhangboyu.github.io/
    https://pages.cs.wisc.edu/~csverma/CS766_09/HDRI/hdr.html
https://github.com/vivianhylee/high-dynamic-range-image/blob/master/hdr.py
https://docs.opencv.org/4.x/d3/db7/tutorial_hdr_imaging.html
https://en.wikipedia.org/wiki/Gamma_correction
"""

"""
The dynamic range is the intensity of light or luminance in an image.
Tone mapping deals with varying the intensities of an image to a higher level or high dynamic range.
Tone mapping is a digital image processing technique in which one set of colors is mapped to another in order to create high dynamic range.
"""
