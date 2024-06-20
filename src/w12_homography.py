"""
Homographies
    Track objects


Keypoints:
    - Distinctiveness
    - Scale and Rotation Invariance
    - Localization
    - Stability

    - Harris Corner Detector
    - SIFT (Scale-Invariant Feature Transform)
    - FAST (Features from Accelerated Segment Test)
    - ORB (Oriented FAST and Rotated BRIEF)

Descriptor
    - Robustness
    - Uniqueness
    - Compactness
    - Invariance

    - SIFT Descriptor
    - SURF Descriptor (Speeded-Up Robust Features)
    - BRIEF Descriptor (Binary Robust Independent Elementary Features)
    - ORB Descriptor (Oriented FAST and Rotated BRIEF)

https://www.tutorialspoint.com/opencv-python-matching-the-key-points-of-two-images-using-orb-and-bfmatcher
https://www.geeksforgeeks.org/feature-matching-using-orb-algorithm-in-python-opencv/
https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('./chess_normal.jpg', cv2.IMREAD_GRAYSCALE)   
img2 = cv2.imread('./chess_rotated.jpg', cv2.IMREAD_GRAYSCALE)

detector = cv2.ORB_create()      # SIFT_create

kp1, desc_1 = detector.detectAndCompute(img1, None)
kp2, desc_2 = detector.detectAndCompute(img2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

matches = bf.match(desc_1,desc_2)

try:
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)
except:
    good_matches = matches[:50]

# matching_result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, flags=2)
matching_result = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=0)    # cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS

plt.figure(figsize=(15, 15))
plt.imshow(matching_result)
plt.axis('off')
plt.show()
