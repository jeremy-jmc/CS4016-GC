import sys
import os
import math
import numpy as np
import cv2
import matplotlib.pyplot as plt

colors_rgb = [
    (0, 0, 0),    # black
    (255, 255, 255),  # white
    (255, 0, 0),  # red
    (0, 255, 0),  # green
    (0, 0, 255),  # blue
    (255, 255, 0)  # yellow
]

def exercise02(img_shape: tuple, n_cells: tuple, working_dir: str):
    channels = 3
    h_pixels, w_pixels = img_shape
    h_cells, w_cells = n_cells

    h_cell_pixels = math.ceil(h_pixels / h_cells)
    w_cell_pixels = math.ceil(w_pixels / w_cells)

    h_init = h_cell_pixels * h_cells
    w_init = w_cell_pixels * w_cells

    board_shape = (h_cells, w_cells, h_cell_pixels, w_cell_pixels, channels)
    board = np.full(board_shape, 255, dtype='uint8')
    
    for i in range(h_cells):
        for j in range(w_cells):
            color = colors_rgb[(i + j) % len(colors_rgb)]
            board[i, j, :, :] = color

    target_shape = (h_init, w_init, channels)
    board = np.reshape(np.transpose(board, (0, 2, 1, 3, 4)), target_shape)
    
    board = board[:h_pixels, :w_pixels, :]
    # board = cv2.cvtColor(board, cv2.COLOR_RGB2BGR)
    # plt.imshow(board)
    # plt.axis('off')
    # plt.show()
    board_filename = f'board_{h_pixels}_{h_cells}_{w_pixels}_{w_cells}.png'
    cv2.imwrite(os.path.join(working_dir, board_filename), board)

    # print(board.shape)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python solution.py <H_PIXELS> <W_PIXELS> <H_CELSS> <W_CELLS>")
        sys.exit('Invalid number of arguments')
    

    working_dir = os.path.join(os.path.dirname(sys.argv[0]), 'output')
    os.makedirs(working_dir, exist_ok=True)

    h_pixels = int(sys.argv[1])
    w_pixels = int(sys.argv[2])

    h_cells = int(sys.argv[3])
    w_cells = int(sys.argv[4])

    img_shape = (h_pixels, w_pixels)
    n_cells = (h_cells, w_cells)

    exercise02(img_shape, n_cells, working_dir)
