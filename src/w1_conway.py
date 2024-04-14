import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

def generate_frame(grid: np.array) -> np.array:
    new_frame = grid.copy()
    height, width = grid.shape

    for i in range(height):
        for j in range(width):
            live_neighbors = np.sum(grid[max(0, i-1):min(height, i+2), max(0, j-1):min(width, j+2)]) - grid[i, j]

            if grid[i, j] == 1:
                # underpopulation or overpopulation
                if live_neighbors < 2 or live_neighbors > 3:
                    new_frame[i, j] = 0
            else:
                # reproduction
                if live_neighbors == 3:
                    new_frame[i, j] = 1
    
    return new_frame * 255

N = 100
M = 100
grid = np.random.choice([0, 1], (N, M), True, [0.85, 0.15]).astype('uint8')
print(grid.shape)
plt.imshow(grid, cmap='gray')
plt.axis('off')
plt.show()

cv2.namedWindow("Conway's Game of Life", cv2.WINDOW_NORMAL)
while True:
    frame = generate_frame(grid)
    grid = frame // 255

    cv2.imshow("Conway's Game of Life", frame)
    key = cv2.waitKey(100)

    if key == ord('q'):
        break
    time.sleep(.5)

cv2.destroyAllWindows()